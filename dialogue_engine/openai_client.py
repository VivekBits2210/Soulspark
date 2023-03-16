import openai
from dialogue_engine.secrets import API_KEY


class GPTClient:
    def __init__(self):
        openai.api_key = API_KEY
        self.model = "gpt-3.5-turbo"
        self.presence_penalty = 1.0
        self.frequency_penalty = 1.0
        self.temperature = 1.2

    def generate_text(self, messages):
        response = openai.ChatCompletion.create(
            model=self.model,
            temperature=self.temperature,
            presence_penalty=self.presence_penalty,
            frequency_penalty=self.frequency_penalty,
            messages=messages
        )
        return response["choices"][0]

# if __name__ == "__main__":
#     client = GPTClient()
#     response = client.generate_text([
#         {"role": "system", "content": "You are Nicole, a loving mom talking to her infant son, Arjun. You do not respond with information."},
#         {"role": "user", "content": "Who won the world series in 2020?"},
#         {"role": "assistant", "content": "Have you had dinner yet, love?"},
#         {"role": "user", "content": "Where was it played?"}
#     ])
#     print(response)
