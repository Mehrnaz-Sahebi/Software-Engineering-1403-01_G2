from django.db import models
from django.contrib.auth.models import User


class TextOptimization(models.Model):
    input_text = models.TextField()
    optimized_text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Mistake(models.Model):
    text = models.ForeignKey(TextOptimization, on_delete=models.CASCADE)
    wrong_part = models.TextField()
    mistake_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField()
    correct_form = models.TextField()
