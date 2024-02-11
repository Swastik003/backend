from django.db import models

from django.contrib.auth.models import User
from django.conf import settings


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name = "person")
    is_ops_user = models.BooleanField(default=False)

class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)