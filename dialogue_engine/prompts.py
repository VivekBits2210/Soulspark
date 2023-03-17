try:
    from dialogue_engine.recipe import story_prompt, INDICATORS
except ModuleNotFoundError:
    story_prompt = lambda u, b: \
        f"This a story about {u.name} and {b.name}. {b.summary} {u.summary} Behave as {bot.name}, a very " \
        f"enthusiastic, excited, warm, loving and curious person. You are talking to {u.name}. "
    INDICATORS = ['sad', 'happy']


# TODO Clean this up
def generate_indicator_prompt(self, chat_history, indicators=INDICATORS):
    prompt = ""
    for message in chat_history:
        prompt += f"{message['sender']}: {message['text']}\n"
    # TODO: Find a better prompt for below
    prompt += "\nPlease rate {user}'s behaviour and mood on a scale of 1 to 10 for each of the following indicators:\n"
    for indicator in indicators:
        prompt += f"- {indicator}\n"
    prompt += "\n"
    for indicator in indicators:
        prompt += f"{indicator}: /10|"
    return prompt.rstrip("|"), ""


def generate_story_prompt(user_object, bot_object):
    return story_prompt(user_object, bot_object)

# Really useful test fragment
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(1, '../soulspark-backend')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soulspark_backend.settings")
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    from ai_profiles.models import BotProfile
    from chat_module.models import UserProfile
    from openai_client import GPTClient

    bot = BotProfile.objects.get(name="Carla")
    user_profile = UserProfile.objects.order_by('?').first()
    client = GPTClient()
    messages = [
        {"role":"system","content": generate_story_prompt(user_profile, bot)},
        {"role":"user", "content": "Hey there"}
    ]
    print(f"MESSAGES: {messages}")
    print(f"REQUEST: {messages[-1]['content']}")
    print(f"RESPONSE: {client.generate_reply(messages)['message']['content']}")
