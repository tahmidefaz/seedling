"""Reads and validates YAML files containing topic and intent information"""

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
                    "entities": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "type": {"type": "string"},
                                "description": {"type": "string"},
                            },
                            "required": ["name", "type", "description"],
                            "additionalProperties": False,
                        }
                    }
                },
                "required": ["name", "description"],
                "additionalProperties": False,
            }
        }
    },
    "required": ["name", "description", "intents"],
    "additionalProperties": False,
}


def is_valid(filename: str, data: dict) -> bool:
    """Validates data against a JSON schema.

    Args:
        filename: The name of the file being validated.
        data: The file data to validate.

    Returns:
        True if the data is valid, False otherwise.
    """
    try:
        jsonschema.validate(instance=data, schema=SCHEMA)
    except jsonschema.exceptions.ValidationError as e:
        print(f"{filename} is invalid: {e}")
        return False
    return True


def read(directory: str) -> list:
    """Reads YAML files in a directory, validates it using a JSONschema
        and returns an array of dictionaries.

    Args:
        directory: The path to the directory containing the YAML files.

    Returns:
        An array of dictionaries, where each dictionary represents the content of a YAML file.
    """

    yaml_files = glob.glob(f"{directory}/*.yaml")
    all_topic_info = []

    for yaml_file in yaml_files:
        with open(yaml_file, 'r', encoding='UTF-8') as f:
            data = yaml.safe_load(f)
            if is_valid(yaml_file, data):
                all_topic_info.append(data)

    return all_topic_info
