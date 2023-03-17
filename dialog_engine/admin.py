from django.contrib import admin

# Register your models here.
from dialog_engine.models import GPTUsageRecord

admin.site.register(GPTUsageRecord)