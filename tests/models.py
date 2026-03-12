from django.db import models
from django.contrib.auth.models import User

class Test(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField()

    pdf_file = models.FileField(upload_to="tests/")

    question_count = models.IntegerField()

    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

class Question(models.Model):

    ANSWERS = (
        ('A','A'),
        ('B','B'),
        ('C','C'),
        ('D','D'),
    )

    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    number = models.IntegerField()

    correct_answer = models.CharField(max_length=1, choices=ANSWERS)