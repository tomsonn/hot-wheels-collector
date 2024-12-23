from typing import Any

import yaml


def load_yaml(file_path: str) -> Any:
    with open(file_path) as file:
        return yaml.safe_load(file)
