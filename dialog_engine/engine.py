from dialog_engine.openai_client import GPTClient
from dialog_engine.components import Components
from dialog_engine.models import GPTUsageRecord
from dialog_engine.tasks import summarizer


class DialogEngine:
    def __init__(self, user_profile, chat_history_record):
        self.user_profile = user_profile
        self.bot = chat_history_record.bot
        self.chat_history_record = chat_history_record
        self.chat_history = chat_history_record.history
        self.client = GPTClient()
        self.components = Components(user_profile, self.bot, self.chat_history)

    def run(self, summarizer_limit=3500):
        messages, customizations = self.components.generate_indicator_prompt()
        self.client.customize_model_parameters(customizations)
        indicator_message, indicator_tokens = self.client.generate_reply(messages)

        indicator_dict = self.components.parse_indicator_message(indicator_message)
        indicator_vector = tuple(
            indicator_dict[key] for key in sorted(indicator_dict.keys())
        )

        hook = self.components.fetch_template(
            self.components.find_region(indicator_vector)
        )
        user_summary = self.chat_history_record.user_summary
        bot_summary = self.chat_history_record.bot_summary
        messages, customizations = self.components.generate_story_prompt(hook, user_summary, bot_summary)
        self.client.customize_model_parameters(customizations)
        response, story_tokens = self.client.generate_reply(messages)

        if story_tokens > summarizer_limit:
            summarizer.delay(self.client, self.components, self.chat_history_record)

        usage_record = GPTUsageRecord.objects.create(
            user=self.user_profile.user,
            bot=self.bot,
            indicator_tokens=indicator_tokens,
            story_tokens=story_tokens,
            total_tokens=indicator_tokens + story_tokens,
            indicator_vector=indicator_vector,
            indicator_version="v1",
            chat_history_length=len(self.chat_history),
        )
        print(usage_record)
        return response

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
#     from chat_module.models import UserProfile, ChatHistory
#     from dialog_engine.models import GPTUsageRecord
#
#     bot = BotProfile.objects.get(name="Carla")
#     user_profile = UserProfile.objects.get(name="Vivek")
#     chat_history = [
#         {"source": "Vivek", "message": "Talk to me; I wanna know more about chess."},
#         {"source": "Carla", "message": "Sure, we can talk about Magnus Carlsen!"},
#         {
#             "source": "Vivek",
#             "message": "Can you imagine actually saying something instead of generic shit.",
#         },
#         {"source": "Carla", "message": "Oh, I'm sorry, we'll figure it out"},
#         {"source": "Vivek", "message": "Tell me something interesting about yourself."},
#     ]
#     chat_history_record=ChatHistory(user=user_profile.user,
#                                     bot=bot,
#                                     history=chat_history)
#
#     qset = GPTUsageRecord.objects.filter(user=user_profile.user,bot=bot,chat_history_length=len(chat_history))
#     if qset.exists():
#         qset.delete()
#
#     engine = DialogEngine(
#         user_profile=user_profile,
#         chat_history_record=chat_history_record
#     )
#     print(
#         f"ENGINE: {engine.run()}"
#     )
