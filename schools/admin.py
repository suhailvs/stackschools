from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import path
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.db.models import Max

from .models import (School,AuditEntry, GeneralSettings)

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    search_fields = ('username', )
    # exclude = ('school',) # to fix: it take 5 seconds to load user change and add

@admin.register(AuditEntry)
class AuditEntryAdmin(admin.ModelAdmin):
    readonly_fields = ['log_time',]
    list_display = ['action', 'username', 'log_time',]
    list_filter = ['action',]

admin.site.register(get_user_model(), UserAdmin)
admin.site.register(School)
admin.site.register(GeneralSettings)