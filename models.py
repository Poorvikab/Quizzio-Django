from django.db import models
from django.contrib.auth.models import User
import random

def generate_quiz_code():
    """Generates a unique 5-digit random quiz code."""
    while True:
        code = str(random.randint(10000, 99999))
        if not Quiz.objects.filter(quiz_code=code).exists():  # ✅ Ensures uniqueness
            return code


class Folder(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders')

    def __str__(self):
        return self.name

class Quiz(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="quizzes")
    quiz_code = models.CharField(max_length=5, unique=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.quiz_code:
            self.quiz_code = generate_quiz_code()  # Generate unique 5-digit code
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.folder.name} - {self.quiz_code}"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=500)
    options = models.JSONField()  # Stores {"A": "Option A", "B": "Option B", "C": "Option C"}
    correct_option = models.CharField(max_length=1, choices=[("A", "A"), ("B", "B"), ("C", "C")])

    def __str__(self):
        return f"{self.text} ({self.quiz.quiz_code})"