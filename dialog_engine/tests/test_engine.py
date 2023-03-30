from rest_framework.test import APITestCase
from chat_module.models import ChatHistory
from chat_module.tests.utils import create_bot, create_user_and_profile
from dialog_engine.engine import DialogEngine
import logging

logger = logging.getLogger("my_logger")


class EngineTestCase(APITestCase):
    def setUp(self):
        self.user, self.encrypted_email, self.user_profile = create_user_and_profile(
            first_name="Vivek"
        )
        self.bot = create_bot(name="Carla")
        self.valid_messages = [
            {"who": "Vivek", "message": "What should we talk about"},
            {"who": "Carla", "message": "I dunno, pretend to say something"},
            {"who": "Vivek", "message": "This is me saying things"},
            {
                "who": "Carla",
                "message": "I like the things you said, those are definitely things that were said.",
            },
            {
                "who": "Vivek",
                "message": "This is the last message that is summarized before, now the convo starts.",
            },
            {"who": "Carla", "message": "Hey there! What a nice, sunny day."},
            {"who": "Carla", "message": "What are you doing today?"},
            {
                "who": "Vivek",
                "message": "Talking to my friends, we're going on a trek this Thursday",
            },
            {
                "who": "Carla",
                "message": "Wow, I love treks! Here in Boulder, we have the best trekking routes.",
            },
            {
                "who": "Vivek",
                "message": "Nice! I really like trekking too. I also like to make chicken curry",
            },
            {"who": "Carla", "message": "Oh, how often do you eat chicken curry"},
            {
                "who": "Vivek",
                "message": "Around twice a week, it's usually too expensive these days.",
            },
            {
                "who": "Carla",
                "message": "That's sad; hopefully one day you can afford more chicken curry",
            },
            {
                "who": "Vivek",
                "message": "Yeah, I'm headed to an internship this summer; that should help pay for things",
            },
            {"who": "Carla", "message": "Ooh nice, where are you headed?"},
            {
                "who": "Vivek",
                "message": "I'm working at SoulSpark, it's a long form AI friend company.",
            },
            {
                "who": "Carla",
                "message": "Sounds fancy! I'm not really into programming; I like chess a lot more",
            },
            {"who": "Vivek", "message": "Me too, what's your favourite opening?"},
            {
                "who": "Carla",
                "message": "I have been trying out the Scandinavian Defense. The development is slow, but black finds an advantage later in the game.",
            },
            {"who": "Vivek", "message": "That's cool"},
            {"who": "Carla", "message": "Yeah"},
            {
                "who": "Vivek",
                "message": "This is the first message that should not be included in the summary",
            },
            {
                "who": "Carla",
                "message": "Yeah, you're right, now we are in the second message",
            },
            {
                "who": "Vivek",
                "message": "So Carla, where should I go during my summer?",
            },
        ]
        self.valid_bot_summary = [
            "Carla loves chess.",
            "Carla thinks Vivek is funny.",
            "Carla wants to visit France someday.",
            "Carla is baking a cake tomorrow.",
        ]
        self.valid_user_summary = [
            "Vivek is working on a coding project.",
            "Vivek will answer an exam on 25th March.",
            "Vivek loves to cook chicken curry.",
            "Vivek wants to visit Japan someday.",
        ]
        self.valid_summary_index = 4

    def test_engine_clean_run(self):
        chat_history_record = ChatHistory(
            user=self.user,
            bot=self.bot,
            history=self.valid_messages,
            user_summary=self.valid_user_summary,
            bot_summary=self.valid_bot_summary,
            summary_index=self.valid_summary_index,
        )
        chat_history_record.save()
        engine = DialogEngine(
            user_profile=self.user_profile, chat_history_record=chat_history_record
        )
        logger.info(f"Engine: {engine.run()}")
