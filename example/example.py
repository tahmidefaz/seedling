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
    # print("Name:", intent_info["name"])
    # print("Description", intent_info["description"])
  return topic_to_tools

def get_intent_tools(topic_info, topic):
  intent_to_tools = []

  intents = []
  for t in topic_info:
    if t['name'] == topic:
      intents = t['intents']

  for intent in intents:
    intent_to_tools.append({
      'type': 'function',
      'function': {
        'name': intent['name'],
        'description': intent['description']
      },
    })

  return intent_to_tools

# Example usage:
directory = "example_yamls"
full_intent_info = read_yaml_files(directory)

topic_tools = get_tools_from_topic(full_intent_info)


user_message = 'I want to fly to Rome.'
print("User query:", user_message)

client = OpenAI(
  base_url = 'http://localhost:11434/v1',
  api_key='ollama', # required, but unused
)

completion = client.chat.completions.create(
  model='llama3.1',
  messages=[{'role': 'user', 'content': user_message}],

  tools=topic_tools
)

chosen_topic = completion.choices[0].message.tool_calls[0].function.name

print("predicted topic:", chosen_topic)

intent_tools = get_intent_tools(full_intent_info, chosen_topic)

completion = client.chat.completions.create(
  model='llama3.1',
  messages=[{'role': 'user', 'content': user_message}],

  tools=intent_tools
)

chosen_intent = completion.choices[0].message.tool_calls[0].function.name

print("predicted intent:", chosen_intent)
