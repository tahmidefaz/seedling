"""Used to predict the intent using LLM."""

from .prep import get_tools_from_topics, get_tools_from_intents
from .language_model import LanguageModel


def predict(
        llm: LanguageModel,
        all_topic_info: dict,
        user_message: str
        ) -> dict:
    """Predicts the topic and intent of a user message.

    Args:
        llm: A LanguageModel instance for generating completions.
        all_topic_info: A dictionary containing all available topic and intent information.
        user_message: The user's input message as a string.

    Returns:
        A dictionary containing the predicted topic and intent.
    """
    topic_tools = get_tools_from_topics(all_topic_info)

    topic_completion = llm.completion(user_message, topic_tools)

    chosen_topic = llm.extract_choice(topic_completion, None)

    intent_tools = get_tools_from_intents(all_topic_info, chosen_topic)

    intent_completion = llm.completion(user_message, intent_tools)
    chosen_intent_info = llm.extract_choice(intent_completion, intent_tools)

    predicted = {
        "topic": chosen_topic,
        "intent": chosen_intent_info["name"],
        "entities": chosen_intent_info["params"]
    }

    return predicted
