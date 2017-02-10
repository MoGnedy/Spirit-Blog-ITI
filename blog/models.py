from __future__ import unicode_literals

from django.utils import timezone

from django.db import models
from django.conf import settings

import datetime


# Notes please indentations with tabs .. 1 line between imports & two lines before and after classes or functions
# Models

from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True


# categories
class Category(models.Model):
    categoryName = models.CharField(max_length=200)
    users = models.ManyToManyField(User, null=True, blank=True)

    def __str__(self):
        return self.categoryName
# Posts
class Post(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    image=models.ImageField(upload_to = './static/img/')
    content=models.TextField()
    category=models.ForeignKey(Category)
    user=models.ForeignKey(settings.AUTH_USER_MODEL)


# Comment
class Comment(models.Model):
    comment_text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
# Reply
class Reply(models.Model):
    replay_text=models.TextField(max_length=250, null =True)
    pub_date = models.DateTimeField(auto_now_add=True, null = True,editable=True)
    post = models.ForeignKey(Post)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True)
    comment=models.ForeignKey(Comment)



class ForbiddenWords(models.Model):
    forbiddenWord = models.CharField(max_length = 180)