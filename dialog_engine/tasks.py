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
            if len(summary_line) < 5:
                continue
            if current_name in summaries:
                summaries[current_name].append(summary_line)
            else:
                summaries[current_name] = [summary_line]

    return summaries


# TODO: Test case: Issues when we hit token limits before 10 messages? Possible?
# TODO: Issue with a fast typer? What if multiple summarization calls are made? (need to prevent this from happening)
def summarizer(client, components, chat_history_record, usage_record, keep_limit=5):
    summarizer_tokens = 0
    messages, customizations = components.generate_summarization_prompt(keep_limit=keep_limit,
                                                                        summary_index=chat_history_record.summary_index)
    if len(messages)==1:
        return

    client.customize_model_parameters(customizations)
    summary, cost = client.generate_reply(messages)
    summarizer_tokens += cost

    summaries = parse_summary(summary)
    chat_history_record.user_summary.extend(summaries['user'])
    chat_history_record.bot_summary.extend(summaries['bot'])

    messages, customizations = components.consolidate_summarization_prompt(chat_history_record.user_summary)
    client.customize_model_parameters(customizations)
    consol_summary, cost = client.generate_reply(messages)
    summarizer_tokens += cost
    chat_history_record.user_summary = parse_summary(consol_summary)['default']

    messages, customizations = components.consolidate_summarization_prompt(chat_history_record.bot_summary)
    client.customize_model_parameters(customizations)
    consol_summary, cost = client.generate_reply(messages)
    summarizer_tokens += cost
    chat_history_record.bot_summary = parse_summary(consol_summary)['default']

    chat_history_record.summary_index = max(-1,len(chat_history_record.history)-keep_limit-1)
    usage_record.summarizer_tokens = summarizer_tokens
    usage_record.save()
    chat_history_record.save()
