from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):

    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)