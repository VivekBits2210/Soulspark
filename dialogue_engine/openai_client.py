import openai


# TODO: Update this for ChatGPT style API
class GPTClient:
    def __init__(self, api_key):
        openai.api_key = api_key
        self.model_engine = "text-davinci-002"

    def generate_text(self, prompt, max_tokens=50, temperature=0.5):
        response = openai.Completion.create(
            engine=self.model_engine,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )
        message = response.choices[0].text.strip()
        return message
