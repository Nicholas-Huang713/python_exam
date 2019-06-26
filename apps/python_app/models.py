from __future__ import unicode_literals
from django.db import models
from datetime import date, datetime
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile(r'.{8,}')

class UserManager(models.Manager):
    def user_validator(self,postData):
        errors = {}
        if len(postData['name']) < 2:
            errors['name'] = "Name must be at least 2 characters."
        if len(postData['alias']) < 2:
            errors['alias'] = "Alias must be at least 2 characters."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email."
        if not PW_REGEX.match(postData['password']):
            errors['password'] = "Password must be at least 8 characters long."
        if postData['password'] != postData['confirm_password']:
            errors['verified'] = "Passwords do not match!"
        return errors

class User(models.Model):
    name = models.CharField(max_length= 45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors={}
        if len(postData['quoted_by']) < 4:
            errors['quoted_by'] = "Name must be at least 3 characters."
        if len(postData['message']) < 10:
            errors['message'] = "Message must be at least 10 characters."
        return errors

class Quote(models.Model):
    quoted_by = models.CharField(max_length= 45)
    message = models.CharField(max_length=255)
    users = models.ForeignKey(User, related_name="quotes")
    join = models.ManyToManyField(User, related_name="join")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()