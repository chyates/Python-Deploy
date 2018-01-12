# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import date, time, datetime
from time import strptime, strftime, localtime
import bcrypt


class UserManager(models.Manager):
    def valid_log(self, postData):
        errors = []
        if len(self.filter(username=postData['username'])) > 0:
            user = self.filter(username=postData['username'])[0]
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors.append("Username and password must match.")
        else:
            errors.append("Username not in the system")

        if errors:
            return errors
        return user

    def valid_reg(self, postData):
        errors = []
        if len(postData['name']) < 3 or len(postData['username']) < 3:
            errors.append("Name or username fields must be at least 3 characters.")
        if any(char.isdigit() for char in postData['name']):
            errors.append("Name field cannot contain numbers.")
        if len(postData['password']) < 8:
            errors.append("Password must be at least 8 characters.")
        if postData['password'] != postData['confirm_password']:
            errors.append("Passwords must match")
        if not errors:
            hashed_pw = bcrypt.hashpw(
                (postData['password'].encode()), bcrypt.gensalt(5))
            new_user = self.create(
                name=postData['name'],
                username=postData['username'],
                password=hashed_pw
            )
            return new_user
        return errors


class TripManager(models.Manager):
    def valid_trip(self, postData):
        errors = []
        if len(postData['destination']) < 1 or len(postData['description']) < 1:
            errors.append("Text fields are required.")

        date_errors = []
        if len(postData['start_date']) < 1:
            errors.append("Start date required")
            date_errors.append("Start date required")

        if len(postData['end_date']) < 1:
            errors.append("End date required")
            date_errors.append("End date required")
            
        if not date_errors:
            current_date = datetime.now()
            start_date = datetime.strptime(postData['start_date'], "%Y-%m-%d")
            end_date = datetime.strptime(postData['end_date'], "%Y-%m-%d")

            if start_date > end_date:
                errors.append("Start date cannot fall before the end date")
            if start_date < current_date:
                errors.append("Start date cannot fall before the current date")

        if not errors and not date_errors:
            new_trip = self.create(
                destination=postData['destination'],
                start_date=start_date,
                end_date=end_date,
                description=postData['description'],
                creator=User.objects.get(id=postData['current_user'])
            )
            return new_trip
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(default='some_string')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    travelers = models.ManyToManyField(User, related_name="trips_joined")
    creator = models.ForeignKey(User, related_name="trips_owned")
    objects = TripManager()