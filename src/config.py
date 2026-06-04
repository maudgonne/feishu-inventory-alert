import json
import os

_DEFAULT = os.path.join(os.path.dirname(__file__), "..", "config.json")


def load_config(path=_DEFAULT):
    with open(path, encoding="utf-8") as f:
        return json.load(f)
