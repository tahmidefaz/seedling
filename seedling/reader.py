import yaml
import glob


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
      all_topic_info.append(data)

  return all_topic_info

