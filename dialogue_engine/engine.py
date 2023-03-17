from dialogue_engine import GPTClient
from dialogue_engine.components import Components


class DialogueEngine:
    def __init__(self, user_profile, bot, chat_history):
        self.user_profile = user_profile
        self.bot = bot
        self.chat_history = chat_history
        self.client = GPTClient()
        self.indicator_limit = 10

    def run(self, message):
        self.chat_history.append(message)
        messages, customizations = generate_indicator_prompt(user_profile=self.user_profile,
                                                             bot=self.bot,
                                                             chat_history=self.chat_history[-self.indicator_limit:])
        self.client.customize_model_parameters(customizations)

        indicator_message = self.client.generate_reply(messages)['message']['content']
        indicator_dict = parse_indicator_message(indicator_message)
        indicator_vector = tuple(indicator_dict[key] for key in sorted(indicator_dict.keys()))

        hook = fetch_template(find_region(indicator_vector))
        messages, customizations = generate_story_prompt(self.user_profile,
                                                         self.bot,
                                                         self.chat_history,
                                                         hook)
        self.client.customize_model_parameters(customizations)
        return self.client.generate_reply(messages)['message']['content']