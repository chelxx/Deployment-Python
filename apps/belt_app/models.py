# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import datetime
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = []
        # Name Length Validation
        if len(postData['first']) < 2: 
            errors.append('First Name should be more than 2 characters.')
        if len(postData['last']) < 2: 
            errors.append('Last Name should be more than 2 characters.')
        if len(postData['alias']) < 2:
            errors.append('Alias should be more than 2 characters.')

        # # Name Character Validation
        if not postData['first'].isalpha():
            errors.append('First Name can only contain letters.')
        if not postData['last'].isalpha():
            errors.append('Last Name can only contain letters.')

        # Password Validation
        if len(postData['password']) < 8:
            errors.append('Password should be longer than 8 characters.')
        if postData['password'] != postData['confirm_password']:
            errors.append('Password do not match.')
        if len(postData['password']) == 0:
            errors.append('Password must be filled out.')

        #Alias Validation
        if len(self.filter(alias = postData['alias'])):
            errors.append('Alias is already in use.')

        #Birthday Validation
        if len(postData['password']) == 0:
            errors.append('Birthday must be filled out.')
        return errors

        #Email Validation
        if len(self.filter(email = postData['email'])):
            errors.append('Email is already in use.')

    def YesToFriendship(self, user_id, friend_id):
        user = self.get(id=user_id)
        friend = self.get(id=friend_id)
        Friend.objects.create(friender=user, friendee=friend)
        Friend.objects.create(friender=friend, friendee=user)

    def NoToFriendship(self, user_id, friend_id):
        user = self.get(id=user_id)
        friend = self.get(id=friend_id)
        friend_connection1 = Friend.objects.filter(friender=user, friendee=friend)
        friend_connection2 = Friend.objects.filter(friender=friend, friendee=user)
        friend_connection1.delete()
        friend_connection2.delete()

class User(models.Model):
    first = models.CharField(max_length=50, default = 'blank')
    last = models.CharField(max_length=50, default = 'blank')
    alias = models.CharField(max_length=50, default = 'blank')
    email = models.CharField(max_length=255, default = 'blank')
    password = models.CharField(max_length=255, default = 'blank')
    birthday = models.DateField(auto_now=False, auto_now_add=False, default='blank')
    friends = models.ManyToManyField('self', related_name='friends')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

#BELT EXAM MODELS HERE:
class Friend(models.Model):
    friender = models.ForeignKey(User, related_name='friender')
    friendee = models.ForeignKey(User, related_name='friendee')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()