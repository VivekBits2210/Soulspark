import logging
from dialog_engine.openai_client import GPTClient
from dialog_engine.components import Components
from dialog_engine.models import GPTUsageRecord
from dialog_engine.tasks import summarizer

logger = logging.getLogger("my_logger")


class DialogEngine:
    def __init__(self, user_profile, chat_history_record):
        self.user_profile = user_profile
        self.bot = chat_history_record.bot
        self.chat_history_record = chat_history_record
        self.chat_history = chat_history_record.history
        self.client = GPTClient()
        self.components = Components(user_profile, self.bot, self.chat_history)

    def run(self, summarizer_limit=3500):
        # messages, customizations = self.components.generate_indicator_prompt()
        # self.client.customize_model_parameters(customizations)
        # logger.info(f"\nIndicator Inputs: {messages}")
        # indicator_message, indicator_tokens = self.client.generate_reply(messages)
        # logger.info(f"Indicator Response: {indicator_message}")
        # indicator_dict = self.components.parse_indicator_message(indicator_message)
        # logger.info(f"Indicator Dict: {indicator_dict}")
        # indicator_vector = tuple(
        #     indicator_dict[key] for key in sorted(indicator_dict.keys())
        # )
        #
        # hook = self.components.fetch_template(
        #     self.components.find_region(indicator_vector)
        # )
        # logger.info(f"Hook: {hook}")
        user_summary = self.chat_history_record.user_summary
        bot_summary = self.chat_history_record.bot_summary
        logger.info(f"User Summary: {user_summary}")
        logger.info(f"Bot Summary: {bot_summary}")

        messages, customizations = self.components.generate_story_prompt(
            user_summary, bot_summary
        )
        self.client.customize_model_parameters(customizations)
        response, story_tokens = self.client.generate_reply(messages)
        logger.info(f"Story Response: {response}")

        usage_record = GPTUsageRecord.objects.create(
            email=self.user_profile.user.email,
            bot_name=self.bot.name,
            indicator_tokens=0,
            story_tokens=story_tokens,
            indicator_vector="[]",
            indicator_version="v1",
            chat_history_length=len(self.chat_history),
        )
        logger.info(f"GPT Usage: {usage_record}")

        if story_tokens > summarizer_limit:
            summarizer.delay(
                self.client, self.components, self.chat_history_record, usage_record
            )

        tokens = response.split(":", 1)
        response_string = tokens[0] if len(tokens) == 1 else tokens[1]
        return response_string
