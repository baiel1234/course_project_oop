from django.db import models
from django.contrib.auth.models import User
from tests.models import Test

class Result(models.Model):

    student = models.ForeignKey(User, on_delete=models.CASCADE)

    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    score = models.IntegerField()

    total = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)