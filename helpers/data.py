import json

def load_data(file = "data.json"):
    with open(file, "r") as f:
        data = json.load(f)

    return (data["subreddit"], data["trigger"], data["script"], data["footer"])