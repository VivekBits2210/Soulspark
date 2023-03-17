import random

try:
    from dialogue_engine.recipe import \
        construct_story_system_message, \
        construct_indicator_system_message, \
        construct_summarization_system_message, \
        regions, \
        templates, \
        INDICATORS
except ModuleNotFoundError:
    construct_story_system_message = lambda u, b: \
                                         f"This is a story about {u.name} and {b.name}. {b.summary} {u.summary} " \
                                         f"Behave as {b.name}, a very " \
                                         f"enthusiastic, excited, warm, loving and curious person. " \
                                         f"You are talking to {u.name}. ", {}
    construct_indicator_system_message = lambda u, b: "Randomly fill values for x1,x2...xn: " \
                                                      "'sadness:x1/10|happiness:x2/10'", \
                                         {'temperature': 0}
    construct_summarization_system_message = lambda u, b: "Summarize the conversation.", {'temperature': 0.7}
    regions = []
    templates = {}

    INDICATORS = ['sad', 'happy']


def construct_conversation_from_chat_history(chat_history):
    conversation = ""
    for entry in chat_history:
        conversation += f"{entry['source']}: {entry['message']}\n"
    return conversation


def generate_indicator_prompt(user_profile, bot, chat_history, indicators=INDICATORS):
    prompt, api_customizations = construct_indicator_system_message(user_profile, bot, indicators)

    # TODO: Check performance improvement when below prompt is few-shotted
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": construct_conversation_from_chat_history(chat_history)}
    ]
    return messages, api_customizations


def generate_story_prompt(user_profile, bot):
    prompt, api_customizations = construct_story_system_message(user_profile, bot)
    messages = [
        {"role": "system", "content": prompt}
    ]
    return messages, api_customizations


def generate_summarization_prompt(user_profile, bot):
    prompt, api_customizations = construct_summarization_system_message(user_profile, bot)
    messages = [
        {"role": "system", "content": prompt}
    ]
    return messages, api_customizations


def parse_indicator_message(message_text):
    indicator_mapping = {}
    for indicator in message_text.split("|"):
        name, value = indicator.split(":")
        numerator, denominator = value.split("/")
        indicator_mapping[name] = int(numerator) * 10 // int(denominator)
    return indicator_mapping


def find_region(regions, indicator_vector):
    """
    Finds the region a given point belongs to in an N-dimensional space.

    Returns:
    int: The index of the region the point belongs to, or -1 if the point does not belong to any region.
    """
    for i, region in enumerate(regions):
        lower_bounds, upper_bounds = region
        if all(lower_bound <= coord <= upper_bound for lower_bound, upper_bound, coord in
               zip(lower_bounds, upper_bounds, indicator_vector)):
            return i
    return -1


def fetch_template(region_index, templates):
    if region_index == -1:
        return None
    probability_distribution = templates[region_index]
    return random.choices(probability_distribution.keys(), weights=probability_distribution.values())[0]


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
    user_profile = UserProfile.objects.get(name="Vivek")
    client = GPTClient()

    messages, customizations = generate_story_prompt(user_profile, bot)
    client.customize_model_parameters(customizations)
    messages.extend([{"role": "user", "content": f"{user_profile.name}: Hey there"}])
    print(f"MESSAGES: {messages}")
    print(f"REQUEST: {messages[-1]['content']}")
    print(f"RESPONSE: {client.generate_reply(messages)['message']['content']}")

    chat_history = [
        {'source': 'Vivek', 'message': 'Talk to me'},
        # {'source': 'Carla', 'message': 'What?'},
        {'source': 'Vivek', 'message': 'Can you imagine actually saying something instead of generic shit.'},
        # {'source': 'Carla', 'message': 'Huh?'},
    ]

    messages, customizations = generate_indicator_prompt(user_profile, bot, chat_history)
    client.customize_model_parameters(customizations)
    print(f"MESSAGES: {messages}")
    print(f"RESPONSE: {client.generate_reply(messages)['message']['content']}")
