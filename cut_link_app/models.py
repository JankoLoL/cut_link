from django.db import models
from django.contrib.auth.models import User
import string
import random


class ShortenedUrl(models.Model):
    original_url = models.URLField(max_length=2048)
    shortened_id = models.CharField(max_length=10, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shortened_urls')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.shortened_id:
            self.shortened_id = ShortenedUrl.generate_unique_id()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_id():
        length = 10
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def __str__(self):
        return f"{self.original_url} shortened to {self.shortened_id}"
