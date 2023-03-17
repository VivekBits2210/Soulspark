import openai

try:
    from dialog_engine.secrets import API_KEY
except ModuleNotFoundError:
    API_KEY = "fake-key"


class GPTClient:
    def __init__(self):
        openai.api_key = API_KEY
        self.parameters = {
            "model": "gpt-3.5-turbo",
            "presence_penalty": 1.2,
            "frequency_penalty": 1.2,
            "temperature": 1.5,
        }

    def customize_model_parameters(self, customizations):
        self.parameters.update(customizations)

    def generate_reply(self, messages):
        response = openai.ChatCompletion.create(**self.parameters, messages=messages)
        return response["choices"][0]["message"]["content"], response["usage"]["total_tokens"]


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
