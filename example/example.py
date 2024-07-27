import yaml
import glob

from openai import OpenAI


def read_yaml_files(directory):
  """Reads all YAML files in a directory and returns an array of dictionaries.

  Args:
    directory: The path to the directory containing the YAML files.

  Returns:
    An array of dictionaries, where each dictionary represents the content of a YAML file.
  """

  yaml_files = glob.glob(f"{directory}/*.yaml")
  yaml_data = []

  for yaml_file in yaml_files:
    with open(yaml_file, 'r') as f:
      data = yaml.safe_load(f)
      yaml_data.append(data)

  return yaml_data

def get_tools_from_topic(all_intent_info):
  """Prints the top-level "name" and "description" from each YAML dictionary.

  Args:
    all_intent_info: An array of dictionaries, where each dictionary represents the content of a YAML file.
  """
  topic_to_tools = []
  for intent_info in all_intent_info:
    topic_to_tools.append({
      'type': 'function',
      'function': {
        'name': intent_info['name'],
        'description': intent_info['description']
      },
    })
    print("Name:", intent_info["name"])
    print("Description", intent_info["description"])
  return topic_to_tools

# Example usage:
directory = "example_yamls"
full_intent_info = read_yaml_files(directory)

topic_tools = get_tools_from_topic(full_intent_info)



client = OpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key='ollama', # required, but unused
)

completion = client.chat.completions.create(
    model='llama3.1',
    messages=[{'role': 'user', 'content': 'Is it going to be humid tomorrow?'}],

    # provide a weather checking tool to the model
    tools=topic_tools
)

print("predicted topic:", completion.choices[0].message.tool_calls[0].function.name)
