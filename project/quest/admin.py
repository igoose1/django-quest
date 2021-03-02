#   Copyright 2020-2021 Oskar Sharipov
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.import os

from django.contrib import admin
from django.utils.html import mark_safe
from django_summernote.admin import SummernoteModelAdmin

from .models import Level, Code

class CodeInline(admin.TabularInline):
    model = Code


@admin.register(Level)
class LevelAdmin(SummernoteModelAdmin):
    list_display = ('name', 'content_html', 'codes', 'loadlink')
    summernote_fields = ('content',)
    inlines = [
        CodeInline
    ]

    def content_html(self, obj):
        return mark_safe(obj.content)

    def codes(self, obj):
        return '; '.join(
            Code.objects.filter(level=obj).values_list('string', flat=True)
        )

    def name(self, obj):
        return f'{obj.depth}. {obj.title}'

    def loadlink(self, obj):
        return mark_safe(
            f'<a href={obj.loadlink}>{obj.loadlink}</a>'
        )

