from celery import shared_task


def parse_summary(summary):
    split_str = summary.split('\n')
    current_name = 'default'
    summaries = {}

    for line in split_str:
        if 'summary:' in line:
            current_name = "user" if len(summaries) == 0 else "bot"
            summaries[current_name] = []
        else:
            summary_line = line.split('. ', 1)[-1]
            if current_name in summaries:
                summaries[current_name].append(summary_line)
            else:
                summaries[current_name] = [summary_line]

    return summaries


# TODO: Test case: Issues when we hit token limits before 10 messages? Possible?
# TODO: Issue with a fast typer? What if multiple summarization calls are made? (need to prevent this from happening)
@shared_task
def summarizer(client, components, chat_history_record, keep_limit=10):
    messages, customizations = components.generate_summarization_prompt(keep_limit=keep_limit,
                                                                        summary_index=chat_history_record.summary_index)
    client.customize_model_parameters(customizations)
    summary, cost = client.generate_reply(messages)
    summaries = parse_summary(summary)
    chat_history_record.user_summary.extend(summaries['user'])
    chat_history_record.bot_summary.extend(summaries['bot'])
    chat_history_record.user_summary = parse_summary(
        components.consolidate_summarization_prompt(chat_history_record.user_summary))['default']
    chat_history_record.bot_summary = parse_summary(
        components.consolidate_summarization_prompt(chat_history_record.bot_summary))['default']
    chat_history_record.summary_index = len(chat_history_record.chat_history) - keep_limit
    chat_history_record.save()
