import json
def load_config():
    with open('config.json') as f:
        data = json.load(f)
    return data
