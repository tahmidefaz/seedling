"""Support functions to prepare for LLM call."""


def get_tools_from_topics(all_topic_info: list) -> list:
    """Transforms topic information into tools for the LLM.

    Args:
        all_topic_info: An array of dictionaries, where each dictionary
            represents the topic and the intents under that specific topic.

    Returns:
        An array of LLM compatible tools corresponding to each topics.
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


def get_tools_from_intents(all_topic_info: list, topic: str) -> list:
    """Transforms intent information into tools for the LLM.

    Args:
        all_topic_info: An array of dictionaries, where each dictionary
            represents the topic and the intents under that specific topic.
        topic: The name of the topic to parse intents from.

    Returns:
        An array of LLM compatible tools corresponding to each intents
        under the specified topic.
    """
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
