import random

is_recipe = False
RecipeClass = None
try:
    from dialog_engine.recipe import Recipe

    RecipeClass = Recipe
    is_recipe = True
except ModuleNotFoundError:
    from dialog_engine.recipe_mock import RecipeMock

    RecipeClass = RecipeMock


class Components:
    def __init__(self, user_profile, bot, chat_history, recipe_class=RecipeClass):
        self.user_profile = user_profile
        self.bot = bot
        self.chat_history = chat_history
        self.chat_conversation = self.construct_conversation_from_chat_history()
        self.recipe = (
            recipe_class(user_profile, bot) if is_recipe else RecipeMock(user_profile, bot)
        )

    def construct_conversation_from_chat_history(self, history=None):
        if not history:
            history = self.chat_history

        conversation = ""
        for entry in history:
            conversation += f"{entry['who']}: {entry['message']}\n"
        return conversation if len(conversation) > 0 else None

    def generate_indicator_prompt(self, indicator_limit=10):
        prompt, api_customizations = self.recipe.construct_indicator_system_message()

        # TODO v2: Check performance improvement when below prompt is few-shotted
        messages = [
            {"role": "system", "content": prompt},
        ]
        chat_conversation = self.construct_conversation_from_chat_history(
            history=self.chat_history[-indicator_limit:]
        )
        if chat_conversation != "":
            messages.append({"role": "user", "content": chat_conversation})
        return messages, api_customizations

    def generate_story_prompt(self, user_summary, bot_summary, hook=None):
        prompt, api_customizations = self.recipe.construct_story_system_message(self.stringify(user_summary),
                                                                                self.stringify(bot_summary))
        messages = [{"role": "system", "content": prompt}]
        if self.chat_conversation != "":
            messages.append({"role": "user", "content": self.chat_conversation})
        if hook:
            messages.append(
                {
                    "role": "system",
                    "content": f"(Expected reply from {self.bot.name}: {hook})",
                }
            )
        return messages, api_customizations

    def consolidate_summarization_prompt(self, summary):
        prompt, api_customizations = self.recipe.construct_summary_consolidation_system_message()
        messages = [{"role": "system", "content": prompt}]
        if summary and len(summary) > 0:
            messages.append({"role": "user", "content": self.stringify(summary)})
        return messages, api_customizations

    def generate_summarization_prompt(self, keep_limit, summary_index):
        (
            prompt,
            api_customizations,
        ) = self.recipe.construct_summarization_system_message()
        messages = [
            {"role": "system", "content": prompt},
        ]
        if summary_index + 1 <= len(self.chat_history) - keep_limit:
            chat_conversation = self.construct_conversation_from_chat_history(
                history=self.chat_history[summary_index + 1:-keep_limit]
            )
            if chat_conversation != "":
                messages.append({"role": "user", "content": chat_conversation})
        return messages, api_customizations

    def parse_indicator_message(self, message_text):
        indicator_mapping = {}
        for indicator in message_text.split("|"):
            try:
                name, value = indicator.split(":")
            except ValueError:
                continue
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

    def stringify(self, summary):
        result = ""
        for i, item in enumerate(summary):
            result += f"{i + 1}. {item}\n"
        return result

# Really useful test fragment
# if __name__ == "__main__":
#     import sys
#     import os
#     sys.path.insert(1, "../soulspark-backend")
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soulspark_backend.settings")
#     from django.core.wsgi import get_wsgi_application
#
#     application = get_wsgi_application()
#     from ai_profiles.models import BotProfile
#     from chat_module.models import UserProfile
#     from dialog_engine.openai_client import GPTClient
#
#     bot = BotProfile.objects.get(name="Carla")
#     user_profile = UserProfile.objects.get(name="Vivek")
#     client = GPTClient()
#     components = Components(user_profile, bot, [])
#     messages, customizations = components.generate_story_prompt()