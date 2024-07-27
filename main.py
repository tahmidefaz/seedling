from openai import OpenAI

client = OpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key='ollama', # required, but unused
)

completion = client.chat.completions.create(
    model='llama3.1',
    messages=[{'role': 'user', 'content': 'set an alarm for 6am'}],

    # provide a weather checking tool to the model
    tools=[{
      'type': 'function',
      'function': {
        'name': 'get_current_weather',
        'description': 'Get the current weather for a city',
        'parameters': {
          'type': 'object',
          'properties': {
            'city': {
              'type': 'string',
              'description': 'The name of the city. Write "none" if not provided.',
            },
          },
        },
      },
    },
    {
      'type': 'function',
      'function': {
        'name': 'set_alarm',
        'description': 'Sets an alarm for a specific time.',
        'parameters': {
          'type': 'object',
          'properties': {
            'time': {
              'type': 'string',
              'description': 'The alarm time. Write "none" if not provided.',
            },
          },
        },
      },
    },
  ],
)

print(completion.choices[0].message)
