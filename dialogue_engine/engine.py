from dialogue_engine import GPTClient
from dialogue_engine.components import Components


class DialogueEngine:
    def __init__(self, user_profile, bot, chat_history):
        self.user_profile = user_profile
        self.bot = bot
        self.chat_history = chat_history
        self.client = GPTClient()
        self.components = Components(user_profile, bot, chat_history)
        self.indicator_limit = 10

    def run(self, message):
        self.chat_history.append(message)
        messages, customizations = self.components.generate_indicator_prompt()
        self.client.customize_model_parameters(customizations)

        indicator_message = self.client.generate_reply(messages)['message']['content']
        indicator_dict = self.components.parse_indicator_message(indicator_message)
        indicator_vector = tuple(indicator_dict[key] for key in sorted(indicator_dict.keys()))

        hook = self.components.fetch_template(self.components.find_region(indicator_vector))
        messages, customizations = self.components.generate_story_prompt(hook)
        self.client.customize_model_parameters(customizations)
        return self.client.generate_reply(messages)['message']['content']