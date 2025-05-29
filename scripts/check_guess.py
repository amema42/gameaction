import os
import json
import requests

discussion_id = str(os.getenv("DISCUSSION_ID"))
comment_body = os.getenv("COMMENT_BODY", "").strip()
comment_id = os.getenv("COMMENT_ID")
author = os.getenv("COMMENT_AUTHOR")
token = os.getenv("GITHUB_TOKEN")
repo = os.getenv("GITHUB_REPOSITORY")

data_file = "game_data.json"

if not (discussion_id and comment_body and token):
    print("Missing required environment variables.")
    exit(1)

# Only allow numeric guesses
if not comment_body.isdigit():
    print("Comment is not a number, skipping.")
    exit(0)

guess = int(comment_body)

# Load game state
with open(data_file, "r") as f:
    data = json.load(f)

game = data.get(discussion_id)
if not game or game["solved"]:
    print("No game found or already solved.")
    exit(0)

secret = game["secret"]
game["attempts"] += 1

if guess == secret:
    reply = f"🎉 Congrats @{author}! You guessed it right in {game['attempts']} attempts! The number was **{secret}**."
    game["solved"] = True
else:
    reply = f"❌ Nope, {guess} is not the number. Try again!"

# Save updated state
with open(data_file, "w") as f:
    json.dump(data, f, indent=2)

# Post comment reply
api_url = f"https://api.github.com/repos/{repo}/discussions/{discussion_id}/comments"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}
payload = {
    "body": reply,
    "in_reply_to_id": comment_id
}

response = requests.post(api_url, json=payload, headers=headers)
print("Comment response:", response.status_code)
print("Reply body:", reply)
