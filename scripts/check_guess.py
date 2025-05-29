import os
import json
import requests

# Read environment variables
discussion_number = os.getenv("DISCUSSION_NUMBER")
comment_body      = os.getenv("COMMENT_BODY", "").strip()
author            = os.getenv("COMMENT_AUTHOR")
token             = os.getenv("GITHUB_TOKEN")
repo              = os.getenv("GITHUB_REPOSITORY")

data_file = "game_data.json"

# Validate inputs
if not (discussion_number and comment_body and token):
    print("Missing required environment variables.")
    exit(1)
if not comment_body.isdigit():
    print("Comment is not a number, skipping.")
    exit(0)

guess = int(comment_body)

# Load game state
with open(data_file, "r") as f:
    data = json.load(f)

game = data.get(discussion_number)
if not game or game["solved"]:
    print("No game found or already solved.")
    exit(0)

# Update attempts and check guess
secret = game["secret"]
game["attempts"] += 1

if guess == secret:
    reply = (
        f"🎉 Congrats @{author}! "
        f"You guessed it right in {game['attempts']} attempts! "
        f"The number was **{secret}**."
    )
    game["solved"] = True
else:
    reply = f"❌ Nope, {guess} is not the number. Try again!"

# Save updated state
with open(data_file, "w") as f:
    json.dump(data, f, indent=2)

# POST reply via GraphQL API
api_url = "https://api.github.com/graphql"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
    "Content-Type": "application/json"
}

# First, get the discussion ID
discussion_query = """
query($owner: String!, $repo: String!, $number: Int!) {
    repository(owner: $owner, name: $repo) {
        discussion(number: $number) {
            id
        }
    }
}
"""

# Extract owner and repo name from GITHUB_REPOSITORY
owner, repo_name = repo.split('/')

# Query for discussion ID
discussion_payload = {
    "query": discussion_query,
    "variables": {
        "owner": owner,
        "repo": repo_name,
        "number": int(discussion_number)
    }
}

discussion_response = requests.post(api_url, json=discussion_payload, headers=headers)
discussion_data = discussion_response.json()

if "errors" in discussion_data:
    print("Error getting discussion ID:", discussion_data["errors"])
    exit(1)

discussion_id = discussion_data["data"]["repository"]["discussion"]["id"]

# GraphQL mutation for creating a discussion comment
mutation = """
mutation($discussionId: ID!, $body: String!) {
    addDiscussionComment(input: {discussionId: $discussionId, body: $body}) {
        comment {
            id
        }
    }
}
"""

payload = {
    "query": mutation,
    "variables": {
        "discussionId": discussion_id,
        "body": reply
    }
}

response = requests.post(api_url, json=payload, headers=headers)
print("Comment response:", response.status_code, response.text)
print("Reply body:", reply)
