from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11)
    groups = None
    user_permissions = None

    def __str__(self):
        return self.username


class TextOptimizer(models.Model):
    input_text = models.TextField()
    optimized_text = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)




class Mistake(models.Model):
    text = models.ForeignKey(TextOptimizer, on_delete=models.CASCADE)
    wrong_part = models.TextField()
    mistake_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    mistake_made_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    note = models.TextField()

