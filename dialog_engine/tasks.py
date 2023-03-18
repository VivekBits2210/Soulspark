from celery import shared_task
from dialog_engine.engine import DialogEngine


def parse_summary(summary):
    split_str = summary.split('\n')
    current_name = 'default'
    summaries = {}

    for line in split_str:
        if 'summary:' in line:
            current_name = "user" if len(summaries) == 0 else "bot"
            summaries[current_name] = []
        else:
            summaries[current_name].append(line.split('. ', 1)[-1])

    return summaries


# TODO: Test case: Issues when we hit token limits before 10 messages? Possible?
@shared_task
def summarizer(engine: DialogEngine, keep_limit=10):
    chat_history_record = engine.chat_history_record
    messages, customizations = engine.components.generate_summarization_prompt(keep_limit=keep_limit,
                                                                               summary_index=chat_history_record.summary_index)
    engine.client.customize_model_parameters(customizations)
    summary, cost = engine.client.generate_reply(messages)
    summaries = parse_summary(summary)
    chat_history_record.user_summary.extend(summaries['user'])
    chat_history_record.bot_summary.extend(summaries['bot'])
    chat_history_record.user_summary = parse_summary(
        engine.components.consolidate_summarization_prompt(chat_history_record.user_summary))['default']
    chat_history_record.bot_summary = parse_summary(
        engine.components.consolidate_summarization_prompt(chat_history_record.bot_summary))['default']
    chat_history_record.summary_index = len(chat_history_record.chat_history) - keep_limit
    chat_history_record.save()
