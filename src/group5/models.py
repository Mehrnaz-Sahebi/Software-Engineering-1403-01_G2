from django.db import models


class NGram(models.Model):
    dataset_name = models.CharField(max_length=100)
    context = models.TextField()
    word = models.CharField(max_length=100)
    frequency = models.IntegerField()

    def __str__(self):
        return f"{self.dataset_name}: {self.context} -> {self.word} ({self.frequency})"
