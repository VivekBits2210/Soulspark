from dialogue_engine import GPTClient
from dialogue_engine.components import Components


class DialogueEngine:
    def __init__(self, user_profile, bot, chat_history):
        self.user_profile = user_profile
        self.bot = bot
        self.chat_history = chat_history
        self.client = GPTClient()
        self.components = Components(user_profile, bot, chat_history)
        # self.indicator_limit = 10

    def run(self, message):
        self.chat_history.append(message)
        messages, customizations = self.components.generate_indicator_prompt()
        self.client.customize_model_parameters(customizations)
        indicator_message = self.client.generate_reply(messages)["message"]["content"]
        indicator_dict = self.components.parse_indicator_message(indicator_message)
        indicator_vector = tuple(
            indicator_dict[key] for key in sorted(indicator_dict.keys())
        )

        hook = self.components.fetch_template(
            self.components.find_region(indicator_vector)
        )
        messages, customizations = self.components.generate_story_prompt(hook)
        self.client.customize_model_parameters(customizations)
        return self.client.generate_reply(messages)["message"]["content"]

    # TODO: When storing bot messages, always store each sentence in a different message line.
    # TODO: For summarization flow, need to calculate the size of the story prompt in terms of tokens
    # TODO: Once tokens hit some threshold of (tokens/max-allowed), call async summarizer, leave T messages intact at the end
    # TODO: Add Output Limit guardrails to the summarizer prompt


if __name__ == "__main__":
    import sys
    import os

    sys.path.insert(1, "../soulspark-backend")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soulspark_backend.settings")
    from django.core.wsgi import get_wsgi_application

    application = get_wsgi_application()
    from ai_profiles.models import BotProfile
    from chat_module.models import UserProfile
    from dialogue_engine import DialogueEngine

    bot = BotProfile.objects.get(name="Carla")
    user_profile = UserProfile.objects.get(name="Vivek")
    chat_history = [
        {"source": "Vivek", "message": "Talk to me; I wanna know more about chess."},
        {"source": "Carla", "message": "Sure, we can talk about Magnus Carlsen"},
        {
            "source": "Vivek",
            "message": "Can you imagine actually saying something instead of generic shit.",
        },
        {"source": "Carla", "message": "Huh?"},
    ]
    engine = DialogueEngine(
        user_profile=user_profile, bot=bot, chat_history=chat_history
    )
    print(
        f"ENGINE: {engine.run({'source': 'Vivek', 'message': 'Tell me something interesting'})}"
    )
