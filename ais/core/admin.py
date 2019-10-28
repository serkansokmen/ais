from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Question, SentimentResult
from django.utils.translation import gettext as _


class UserAdmin(BaseUserAdmin):
    readonly_fields = ('uuid',)
    list_display = ('uuid', 'username', 'email',
                    'first_name', 'last_name',
                    'is_staff',)


admin.site.register(User, UserAdmin)


class SentimentResultInline(admin.StackedInline):
    model = SentimentResult


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('query', 'user', 'created', 'updated')
    list_filter = ('user',)
    inlines = (SentimentResultInline,)


admin.site.register(Question, QuestionAdmin)
