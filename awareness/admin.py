from django.contrib import admin
from .models import Question, Choice, Attempt, Answer

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('short', 'qtype')
    inlines = [ChoiceInline]

    def short(self, obj):
        return obj.text[:60]

@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_name', 'score', 'total', 'percent', 'created_at')

admin.site.register(Answer)

