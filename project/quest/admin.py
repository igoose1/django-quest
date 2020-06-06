from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Level, Code

class CodeInline(admin.TabularInline):
    model = Code


@admin.register(Level)
class LevelAdmin(SummernoteModelAdmin):
    list_display = ('depth', 'content_length')
    summernote_fields = ('content',)
    inlines = [
        CodeInline
    ]

