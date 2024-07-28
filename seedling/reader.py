import yaml
import glob
import jsonschema

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

def is_valid(filename, data):
  try:
    jsonschema.validate(instance=data, schema=SCHEMA)
  except jsonschema.exceptions.ValidationError as e:
    print(f"{filename} is invalid: {e}")
    return False
  return True


def read(directory):
  """Reads all YAML files in a directory and returns an array of dictionaries.

  Args:
    directory: The path to the directory containing the YAML files.

  Returns:
    An array of dictionaries, where each dictionary represents the content of a YAML file.
  """

  yaml_files = glob.glob(f"{directory}/*.yaml")
  all_topic_info = []

  for yaml_file in yaml_files:
    with open(yaml_file, 'r') as f:
      data = yaml.safe_load(f)
      if is_valid(yaml_file, data):
        all_topic_info.append(data)

  return all_topic_info

