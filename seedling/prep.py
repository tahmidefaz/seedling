def get_tools_from_topics(all_topic_info: dict) -> list:
  """Prints the top-level "name" and "description" from each YAML dictionary.

  Args:
    all_topic_info: An array of dictionaries, where each dictionary represents the content of a YAML file.
  """
  topic_to_tools = []
  for topic_info in all_topic_info:
    topic_to_tools.append({
      'type': 'function',
      'function': {
        'name': topic_info['name'],
        'description': topic_info['description']
      },
    })

  return topic_to_tools

def get_tools_from_intents(all_topic_info: dict, topic: str) -> list:
  intent_to_tools = []

  intents = []
  for topic_info in all_topic_info:
    if topic_info['name'] == topic:
      intents = topic_info['intents']

  for intent in intents:
    intent_to_tools.append({
      'type': 'function',
      'function': {
        'name': intent['name'],
        'description': intent['description']
      },
    })

  return intent_to_tools
