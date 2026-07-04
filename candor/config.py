# candor/config.py
import os
import yaml

DEFAULT_CONFIG = {
    "timeout": 300,
    "logs": {
        "path": os.path.expanduser("~/.candor/logs")
    },
    "nmap": {
        "default_args": ["-Pn"]
    }
}

CONFIG_PATH = os.path.expanduser("~/.candor/config.yaml")

def load_config() -> dict:
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            user_config = yaml.safe_load(f) or {}
        return merge_config(DEFAULT_CONFIG, user_config)
    return DEFAULT_CONFIG

def merge_config(default: dict, user: dict) -> dict:
    merged = default.copy()
    for key, value in user.items():
        if isinstance(value, dict) and key in merged:
            merged[key].update(value)
        else:
            merged[key] = value
    return merged
