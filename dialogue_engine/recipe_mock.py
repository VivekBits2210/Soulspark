class RecipeMock:
    def __init__(self, user_profile, bot):
        self.user_profile = user_profile
        self.bot = bot
        self.regions = []
        self.templates = {}

    def construct_story_system_message(self):
        return (
            f"This is a story about {self.user_profile.name} and {self.bot.name}. {self.bot.summary} {self.user_profile.summary} "
            f"Behave as {self.bot.name}, a very "
            f"enthusiastic, excited, warm, loving and curious person. "
            f"You are talking to {self.user_profile.name}. ",
            {},
        )

    def construct_indicator_system_message(self):
        return (
            "Randomly fill values for x1,x2...xn: " "'sadness:x1/10|happiness:x2/10'",
            {"temperature": 0},
        )

    def construct_summarization_system_message(self):
        return "Summarize the conversation.", {"temperature": 0.7}
