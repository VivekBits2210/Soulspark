from celery import shared_task

from chat_module.models import ChatHistory

# TODO: Add Output Limit guardrails to the summarizer prompt
@shared_task
def summarizer(chat_history_record: ChatHistory):
    pass