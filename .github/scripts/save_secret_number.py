import json
import os
import random

DISCUSSION_ID = os.getenv("DISCUSSION_ID")

if not DISCUSSION_ID:
    raise ValueError("No discussion ID provided")

# file path
data_file = "game_data.json"

# load existing data
if os.path.exists(data_file):
    with open(data_file, "r") as f:
        data = json.load(f)
else:
    data = {}

# if the number has already been generated, do nothing
if DISCUSSION_ID in data:
    print(f"Secret number already exists for discussion {DISCUSSION_ID}")
else:
    secret = random.randint(1, 100)
    data[DISCUSSION_ID] = {
        "secret": secret,
        "attempts": 0,
        "solved": False
    }

    with open(data_file, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Generated secret number {secret} for discussion {DISCUSSION_ID}")
