import datetime

from django.db import models
from django.utils import timezone
from mdeditor.fields import MDTextField

class Page(models.Model):
    page_title = models.CharField(max_length=50)
    page_text = MDTextField(max_length=10000)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.page_title

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Comment(models.Model):
    author_name = models.CharField(max_length=50)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.comment_text

class Exercise(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    exercise_name = models.CharField(max_length=100)
    exercise_href = models.CharField(max_length=200)

    def __str__(self):
        return self.exercise_name