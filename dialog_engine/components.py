import random

is_recipe = False
try:
    from dialog_engine.recipe import Recipe
    is_recipe = True
except ModuleNotFoundError:
    from dialog_engine.recipe_mock import RecipeMock


class Components:
    def __init__(self, user_profile, bot, chat_history):
        self.user_profile = user_profile
        self.bot = bot
        self.chat_history = chat_history
        self.chat_conversation = self.construct_conversation_from_chat_history()
        self.recipe = (
            Recipe(user_profile, bot) if is_recipe else RecipeMock(user_profile, bot)
        )

    def construct_conversation_from_chat_history(self, history=None):
        if not history:
            history = self.chat_history

        conversation = ""
        for entry in history:
            conversation += f"{entry['source']}: {entry['message']}\n"
        return conversation if len(conversation) > 0 else None

    def generate_indicator_prompt(self, indicator_limit=10):
        prompt, api_customizations = self.recipe.construct_indicator_system_message()

        # TODO v2: Check performance improvement when below prompt is few-shotted
        messages = [
            {"role": "system", "content": prompt},
        ]
        chat_conversation = self.construct_conversation_from_chat_history(history=self.chat_history[-indicator_limit:])
        if chat_conversation != "":
            messages.append({"role": "user", "content": chat_conversation})
        return messages, api_customizations

    def generate_story_prompt(self, hook=None):
        prompt, api_customizations = self.recipe.construct_story_system_message()
        messages = [{"role": "system", "content": prompt}]
        if self.chat_conversation != "":
            messages.append({"role": "user", "content": self.chat_conversation})
        if hook:
            messages.append(
                {"role": "system", "content": f"Expected reply from {self.bot.name}: {hook}"}
            )
        return messages, api_customizations

    def generate_summarization_prompt(self):
        (
            prompt,
            api_customizations,
        ) = self.recipe.construct_summarization_system_message()
        messages = [
            {"role": "system", "content": prompt},
        ]
        if self.chat_conversation != "":
            messages.append({"role": "user", "content": self.chat_conversation})
        return messages, api_customizations

    def parse_indicator_message(self, message_text):
        indicator_mapping = {}
        for indicator in message_text.split("|"):
            name, value = indicator.split(":")
            numerator, denominator = value.split("/")
            indicator_mapping[name] = int(numerator) * 10 // int(denominator)
        for indicator in self.recipe.INDICATORS:
            if indicator not in indicator_mapping:
                indicator_mapping[indicator] = 0
        return indicator_mapping

    def find_region(self, indicator_vector):
        for i, region in enumerate(self.recipe.regions):
            lower_bounds, upper_bounds = region
            if all(
                    lower_bound <= coord <= upper_bound
                    for lower_bound, upper_bound, coord in zip(
                        lower_bounds, upper_bounds, indicator_vector
                    )
            ):
                return i
        return -1

    def fetch_template(self, region_index):
        if region_index == -1:
            return None
        probability_distribution = self.recipe.templates[region_index]
        return random.choices(
            probability_distribution.keys(), weights=probability_distribution.values()
        )[0]


# Really useful test fragment
# if __name__ == "__main__":
#     import sys
#     import os
#
#     sys.path.insert(1, "../soulspark-backend")
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soulspark_backend.settings")
#     from django.core.wsgi import get_wsgi_application
#
#     application = get_wsgi_application()
#     from ai_profiles.models import BotProfile
#     from chat_module.models import UserProfile
#     from openai_client _chat_history
#
#     bot = BotProfile.objects.get(name="Carla")
#     user_profile = UserProfile.objects.get(name="Vivek")
#     client = GPTClient()
#     components = Components(user_profile, bot, [])
#
#     messages, customizations = components.generate_story_prompt()
#     client.customize_model_parameters(customizations)
#     messages.extend([{"role": "user", "content": f"{user_profile.name}: Hey there"}])
#     print(f"MESSAGES: {messages}")
#     print(f"REQUEST: {messages[-1]['content']}")
#     print(f"RESPONSE: {client.generate_reply(messages)}")
#
#     chat_history = [
#         {"source": "Vivek", "message": "Talk to me"},
#         {
#             "source": "Vivek",
#             "message": "Can you imagine actually saying something instead of generic shit.",
#         },
#     ]
#
#     components.chat_history = chat_history
#     messages, customizations = components.generate_indicator_prompt()
#     client.customize_model_parameters(customizations)
#     print(f"MESSAGES: {messages}")
#     print(f"RESPONSE: {client.generate_reply(messages)}")
#
#     chat_history = [
#         {"source": "Vivek", "message": "Talk to me; I wanna know more about chess."},
#         {"source": "Carla", "message": "Sure, we can talk about Magnus Carlsen"},
#         {
#             "source": "Vivek",
#             "message": "Can you imagine actually saying something instead of generic shit.",
#         },
#         {"source": "Carla", "message": "Huh?"},
#     ]
#
#     components.chat_history = chat_history
#     messages, customizations = components.generate_summarization_prompt()
#     client.customize_model_parameters(customizations)
#     print(f"MESSAGES: {messages}")
#     print(f"RESPONSE: {client.generate_reply(messages)}")
