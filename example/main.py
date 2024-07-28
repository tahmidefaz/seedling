from seedling import YAMLreader, LanguageModel, predict

def main(user_message):
    all_topics = YAMLreader("example_yamls")

    llm = LanguageModel(
        base_url='http://localhost:11434/v1',
        api_key='ollama',
        model='llama3.1',
    )

    predicted = predict(llm, all_topics, user_message)

    return predicted



if __name__ == "__main__":
    messages = [
        "do some magic on spotify!",
        "I want to make sure that I attend my friend's brithday party later this year",
        "I feel like eating out tonight",
        "It's so dark in this room... I can't see anything... help!",
        "anything interesting happened in the world of AI today?",
        "look for a flight form New York to Los Angeles for July 28th",
        "what's the weather in Seattle today?"
    ]

    for message in messages:
        predicted = main(message)
        print("-----")
        print("MESSAGE:", message)
        print("TOPIC:", predicted["topic"])
        print("INTENT:", predicted["intent"])
        print("ENTITIES", predicted["entities"])
