import logging
import random
import openai
from django.core.exceptions import ValidationError

try:
    from dialog_engine.secrets import API_KEY_LIST
except ModuleNotFoundError:
    API_KEY_LIST = ["fake-key-1", "fake-key-2"]


class GPTClient:
    def __init__(self):
        self.parameters = {
            "model": "gpt-3.5-turbo",
            "presence_penalty": 1.2,
            "frequency_penalty": 1.2,
            "temperature": 1.5,
        }
        self.api_key_list = API_KEY_LIST
        self.ALLOWED_PARAMETERS = {"model": str,
                                   "temperature": float,
                                   "top_p": float,
                                   "max_tokens": int,
                                   "presence_penalty": float,
                                   "frequency_penalty": float,
                                   "logit_bias": dict,
                                   "user": str}

    def customize_model_parameters(self, customizations):
        disallowed_keys = set(customizations) - set(self.ALLOWED_PARAMETERS)
        if disallowed_keys:
            raise ValidationError(f"Parameters {disallowed_keys} are not allowed.")

        for key, value in customizations.items():
            t = self.ALLOWED_PARAMETERS[key]
            if not isinstance(value, t):
                raise ValidationError(f"Value {value} for parameter {key} is of invalid type {type(value)}. "
                                      f"Allowed type is {self.ALLOWED_PARAMETERS[key]}.")
        self.parameters.update(customizations)

    def generate_reply(self, messages, retries=3):
        logging.info(f"Prompt: {messages}")
        openai.api_key = random.choice(self.api_key_list)
        exception_list = []
        for retry in range(retries):
            try:
                response = openai.ChatCompletion.create(**self.parameters, messages=messages)
                return (
                    response["choices"][0]["message"]["content"],
                    response["usage"]["total_tokens"],
                )
            except Exception as e:
                exception_list.append(e)

        error_string = ""
        for retry_index, exception in enumerate(exception_list):
            error_string += f"Retry {retry_index+1}: {repr(exception)}\n"
        raise ValidationError(error_string)

# Test fragment
# if __name__ == "__main__":
#     client = GPTClient()
#     response, _ = client.generate_reply(
#         [
#             {
#                 "role": "system",
#                 "content": "You are Nicole, a loving mom talking to her infant son, George. You do not respond with information.",
#             },
#             {"role": "user", "content": "Who won the world series in 2020?"},
#             {"role": "assistant", "content": "Have you had dinner yet, love?"},
#             {"role": "user", "content": "Where was it played?"},
#         ]
#     )
#     print(response)
