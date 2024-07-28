from openai import OpenAI


class LanguageModel:
    def __init__(self, base_url: str, api_key: str, model: str) -> None:
        self.base_url = base_url
        self.api_key = api_key
        self.model = model

        self.client = OpenAI(
            base_url = self.base_url,
            api_key = self.api_key
        )

    def completion(self, user_message: str, tools: dict) -> dict:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[{'role': 'user', 'content': user_message}],
            tools=tools
        )

        return completion

    def extract_choice(self, completion: dict) -> str:
        try:
            if completion.choices[0].message.tool_calls:
                return completion.choices[0].message.tool_calls[0].function.name
        except Exception as e:
            print(completion)
            print(e)
            return ""
