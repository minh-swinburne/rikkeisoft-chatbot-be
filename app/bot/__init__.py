import os
import json

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

with open(CONFIG_PATH, "r") as file:
    config:dict[str, dict] = json.load(file)


def save_config():
    with open(CONFIG_PATH, "w") as file:
        json.dump(config, file, indent=2)
