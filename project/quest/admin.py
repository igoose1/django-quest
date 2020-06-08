from django.contrib import admin
from django.utils.html import mark_safe
from django_summernote.admin import SummernoteModelAdmin

from .models import Level, Code

class CodeInline(admin.TabularInline):
    model = Code


@admin.register(Level)
class LevelAdmin(SummernoteModelAdmin):
    list_display = ('depth', 'title', 'codes', 'content_html', 'loadlink')
    summernote_fields = ('content',)
    inlines = [
        CodeInline
    ]

    def codes(self, obj):
        return '; '.join(
            Code.objects.filter(level=obj).values_list('string', flat=True)
        )

    def content_html(self, obj):
        return mark_safe(obj.content)

    def loadlink(self, obj):
        return mark_safe(
            f'<a href={obj.loadlink}>{obj.loadlink}</a>'
        )

