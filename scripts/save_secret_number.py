import json
import os
import random

DISCUSSION_NUMBER = os.getenv("DISCUSSION_NUMBER")
if not DISCUSSION_NUMBER:
    raise ValueError("No discussion number provided")

data_file = "game_data.json"

# load existing data
if os.path.exists(data_file):
    with open(data_file, "r") as f:
        data = json.load(f)
else:
    data = {}

# if the number has already been generated, do nothing
if DISCUSSION_NUMBER in data:
    print(f"Secret number already exists for discussion {DISCUSSION_NUMBER}")
else:
    secret = random.randint(1, 100)
    data[DISCUSSION_NUMBER] = {
        "secret": secret,
        "attempts": 0,
        "solved": False
    }
    with open(data_file, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Generated secret number {secret} for discussion {DISCUSSION_NUMBER}")
