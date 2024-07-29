# 🌱 seedling

*A simple and supposedly scalable python library for intent recognition using Large Language Models (LLMs).*


## The Idea

Seedling 🌱 gives you a very simple and scalable way to detect intents from user messages using LLMs.
In order to make things scalable, seedling forces you to group your intents to **topics**.
This also keeps your prompt length short, reduces LLM hallucination, and make things more accurate.

![An image showing intents grouped together into topics](/topics_and_intents.png)

Seedling supports OpenAI/OpenAI-Complatible APIs out of the box.
The OpenAI-Compatible API server must support `tools` use.
It is also very easy to write your own LLM interface for prediction purposes.


### Defining Topic YAML

Following is a simple topic YAML file for the `map` topic with the related intents grouped under it.
Please note that both the topic and the intent `description` must be as detailed as possible, as these get fed into the LLM.

```yaml
name: "map"
description: "Get directions, find places such as restaurants, shops, places of interest, etc."

intents:
  - name: "get_directions"
    description: "Gets directions between two locations."
  - name: "find_place"
    description: "Finds a specific place like a restaurant, gas station, or store."
  - name: "get_traffic_information"
    description: "Gets real-time traffic information for a route."
```


### One-shot entity extraction

In addition to detecting intents, seedling also allows you to attempt to extract entities in one-shot.
For enitity extraction, the smarter you LLM is, the better.

```yaml
name: "travel"
description: "Plan and manage travel arrangements. Search for hotels, flights, and rental cars."

intents:
  - name: "search_flights"
    description: "Searches for flights based on origin, destination, and dates."
    entities:
      - name: "origin"
        type: "string"
        description: "The origin of the flight. Write 'none' if not provided."
      - name: "destination"
        type: "string"
        description: "The destination of the flight.  Write 'none' if not provided."
      - name: "date"
        type: "string"
        description: "The date of the flight. Write 'none' if not provided."
```


## Basic Usage

```python
from seedling import YAMLreader, LanguageModel, predict

# Path to the directory containing all your topic/intent YAML files
all_topics = YAMLreader("directory_path")

# OpenAI/OpenAI-compatible LLM server (must support tools use)
# check example/main.py for Ollama config
llm = LanguageModel(
    base_url='http://baseurl',
    api_key='apikey',
    model='model_name',
)

# Predict the intent of the user message
user_message = "do some magic on spotify!"
predicted = predict(llm, all_topics, user_message)

print(predicted)
```


## Check out the example

Follow the following steps to run the example:

1. Start a virtual environment
    ```
    python -m venv venv
    source venv/bin/activate
    ```
2. Build the library
    ```
    pip install -e .
    ```
3. Install the latest Ollama and pull down the `llama3.1` model.
You can also update the example file under `example/main.py` with your OpenAI/OpenAI-compatible API server information.
4. Run the example
    ```
    cd example
    python main.py
    ```


## Local Development

* Only tested on `python 3.11` so far
* Currently, the actual library source code can be found under `src/seedling`
* To install all dependencies do `pip install ."[dev]"` in your virtual environment
* Use `make lint` to run the linter
