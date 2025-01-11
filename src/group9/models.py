from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.email


class Text(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp for when the text was created

    def __str__(self):
        return f"Text by {self.user.email}"


class Mistake(models.Model):
    text = models.ForeignKey(Text, on_delete=models.CASCADE)
    mistake_type = models.CharField(max_length=255)
    statement = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp for when the mistake was logged

    def __str__(self):
        return f"Mistake in text {self.text.id}"
