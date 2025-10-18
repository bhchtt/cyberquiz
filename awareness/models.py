# models.py
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    TYPE_MCQ = 'MCQ'
    TYPE_TF = 'TF'
    QTYPE_CHOICES = (
        (TYPE_MCQ, 'Multiple Choice'),
        (TYPE_TF, 'True/False'),
    )
    text = models.TextField()
    qtype = models.CharField(max_length=3, choices=QTYPE_CHOICES)
    explanation = models.TextField(blank=True, null=True)
    tf_correct_answer = models.BooleanField(null=True, blank=True)  # для ТФ питань

    def __str__(self):
        return f"{self.text[:60]} ({self.qtype})"

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text[:60]}{' ✅' if self.is_correct else ''}"

class Attempt(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    user_name = models.CharField(max_length=100, blank=True, null=True)
    score = models.IntegerField()
    total = models.IntegerField()
    percent = models.FloatField(default=0.0)  # додаємо дефолт
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        who = self.user.username if self.user else (self.user_name or "Гість")
        return f"{who}: {self.score}/{self.total} ({self.percent}%)"

class Answer(models.Model):
    attempt = models.ForeignKey(Attempt, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, null=True, blank=True, on_delete=models.SET_NULL)
    tf_answer = models.BooleanField(null=True, blank=True)  # True/False для ТФ

    def __str__(self):
        return f"Answer to Q#{self.question.id} in attempt #{self.attempt.id}"


