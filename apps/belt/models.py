from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class Quote(models.Model):
    author = models.CharField(max_length=255)
    content  = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name='quotescreated')
    likes = models.ManyToManyField(User, related_name='likequotes')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

