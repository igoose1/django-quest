from django.contrib import admin

from .models import Level, Code

class CodeInline(admin.TabularInline):
    model = Code


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('depth', 'content_length')
    inlines = [
        CodeInline
    ]

