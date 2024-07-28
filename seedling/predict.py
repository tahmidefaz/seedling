from .prep import get_tools_from_topics, get_tools_from_intents 
from .language_model import LanguageModel

def predict(llm: LanguageModel, all_topic_info: dict, user_message: str) -> dict:
    topic_tools = get_tools_from_topics(all_topic_info)

    topic_completion = llm.completion(user_message, topic_tools)

    chosen_topic = llm.extract_choice(topic_completion)

    intent_tools = get_tools_from_intents(all_topic_info, chosen_topic)

    intent_completion = llm.completion(user_message, intent_tools)
    chosen_intent = llm.extract_choice(intent_completion)

    predicted = {
        "topic": chosen_topic,
        "intent": chosen_intent
    }

    return predicted
