import glob

import jsonschema
import yaml

SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "intents": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                },
                "additionalProperties": False,
            }
        }
    },
    "required": ["name", "description", "intents"],
    "additionalProperties": False,
}


def is_valid(filename: str, data: dict) -> bool:
    try:
        jsonschema.validate(instance=data, schema=SCHEMA)
    except jsonschema.exceptions.ValidationError as e:
        print(f"{filename} is invalid: {e}")
        return False
    return True


def read(directory: str) -> dict:
    """Reads YAML files in a directory and returns an array of dictionaries.

    Args:
        directory: The path to the directory containing the YAML files.

    Returns:
        An array of dictionaries, where each dictionaryrepresents the
        content of a YAML file.
    """

    yaml_files = glob.glob(f"{directory}/*.yaml")
    all_topic_info = []

    for yaml_file in yaml_files:
        with open(yaml_file, 'r', encoding='UTF-8') as f:
            data = yaml.safe_load(f)
            if is_valid(yaml_file, data):
                all_topic_info.append(data)

    return all_topic_info
