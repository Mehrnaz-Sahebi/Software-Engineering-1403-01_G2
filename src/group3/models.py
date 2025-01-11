from django.db import models

class TextOptimization(models.Model):
    input_text = models.TextField()
    optimized_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Optimization on {self.created_at}"
