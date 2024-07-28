"""Defines the LLM interface."""

from openai import OpenAI

from .prep import valid_extracted_tool_params


class LanguageModel:
    """Represents a language model interface.

    Args:
        base_url: The base URL of the language model API.
        api_key: The API key for accessing the language model.
        model: The specific language model to use.
    """
    def __init__(self, base_url: str, api_key: str, model: str) -> None:
        self.base_url = base_url
        self.api_key = api_key
        self.model = model

        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )

    def completion(self, user_message: str, tools: list) -> dict:
        """Generates a response to a user message using the language model.

        This method uses the an OpenAI compatible API to
        complete a conversation based on a user message.

        Args:
            user_message: The message from the user as a string.
            tools: An array of tools to use with the model.

        Returns:
            A dictionary containing the generated response and other details.
        """
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[{'role': 'user', 'content': user_message}],
            tools=tools
        )

        return completion

    def extract_choice(self, completion: dict, tools: list | None) -> str:
        """Extracts the function name from the LLM call in the response.

        Args:
            completion: A dictionary containing the generated response and other details.

        Returns:
            The extracted function name as a string,
            or an empty string if no function name is found or an error occurs.
        """
        try:
            if completion.choices[0].message.tool_calls:
                extracted_tool = completion.choices[0].message.tool_calls[0].function

                if not tools:
                    return extracted_tool.name

                params = {}
                if extracted_tool.arguments:
                    params = valid_extracted_tool_params(extracted_tool, tools)

                intent_info = {
                    'name': extracted_tool.name,
                    'params': params,
                }
                return intent_info
        except Exception as e:    # pylint: disable=broad-exception-caught
            print(completion)
            print(e)
        return ""
