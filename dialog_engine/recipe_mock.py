class RecipeMock:
    def __init__(self, user_profile, bot):
        self.INDICATORS = [
            "sadness",
            "happiness",
        ]
        self.user_profile = user_profile
        self.bot = bot
        self.regions = []
        self.templates = {}

    def construct_story_system_message(self, user_summary, bot_summary):
        return (
            f"This is a story about {self.user_profile.name} and {self.bot.name}. "
            f"Behave as {self.bot.name}, a very "
            f"enthusiastic, excited, warm, loving and curious person. "
            f"You are {self.bot.name}, you are talking to {self.user_profile.name}.",
            {},
        )

    def construct_indicator_system_message(self):
        return (
            f"Given a conversation between {self.bot.name} and {self.user_profile.name}, "
            f"you are an expert who will judge {self.user_profile.name}'s mood " \
            f"along the following indicators: {self.INDICATORS}. Only judge the responses that {self.user_profile.name} sent. " \
            f"Always include every indicator in your response and respond STRICTLY in this format:" \
            f"'<indicator1>:<value1>/10|<indicator2>:<value2>/10....|<indicatorN>:<valueN>/10'",
            {"temperature": 0.0},
        )

    def construct_summarization_system_message(self):
        return "You are a conversation summary assistant. " \
               f"You will output a summary of the conversation STRICTLY in the following format:\n" \
               f"'{self.user_profile.name} summary:\n" \
               f"1. {self.user_profile.name} ... \n" \
               f"2. {self.user_profile.name} ... \n" \
               f"..." \
               f"N. {self.user_profile.name} ... \n" \
               f"{self.bot.name} summary:\n" \
               f"1. {self.bot.name} ... \n" \
               f"2. {self.bot.name} ... \n" \
               f"..." \
               f"P. {self.bot.name} ... '", {"temperature": 0.0}

    def construct_summary_consolidation_system_message(self):
        return "Summarize the summary. You will output a smaller summary STRICTLY in the following format:\n" \
               f"'1. ... \n" \
               f"2. ... \n" \
               f"... \n" \
               f"N.  ... '", {"temperature": 0.0}