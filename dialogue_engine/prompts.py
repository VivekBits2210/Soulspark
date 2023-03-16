INDICATORS = [
    "funny",
    "sad",
    "curious",
    "explicit"
]


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


def generate_story_prompt(self, user_description, bot_description, user_summary, bot_summary, chat_history):
    system_message = f"{bot_description} {user_description}\n\n"  # TODO: fill
    prompt = ""
    for message in chat_history:
        prompt += f"{message['sender']}: {message['text']}\n"
    return prompt, system_message
