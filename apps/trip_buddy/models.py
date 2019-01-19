from django.db import models
from django.contrib import messages
from datetime import date
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def reg_validations(self, postData):
        errors = {}
        if len(postData['first_name']) == 0 or len(postData['last_name']) == 0 or len(postData['email']) == 0 or len(postData['pwd']) == 0 or len(postData['conf_pwd']) == 0:
            errors['required'] = "All fields are required"
            return errors
        if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            errors['length'] = "Name fields must be at least 2 characters"
        if not postData['first_name'].isalpha() or not postData['last_name'].isalpha():
            errors['alpha'] = "Name fields are only letters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email"
        if len(postData['pwd']) < 8:
            errors['pwd'] = "Password must be at least 8 characters"
        if postData['pwd'] != postData['conf_pwd']:
            errors['conf'] = "Passwords don't match"
        if len(User.objects.filter(email=postData['email'])):
            errors['email'] = "Email already exists in database"
        return errors
    
    def login_validation(self, postData):
        errors = {}
        try:
            user = User.objects.get(email=postData['email'])
        except User.DoesNotExist:
            user = None
        if not user or not bcrypt.checkpw(postData['pwd'].encode('utf-8'), user.pwd_hash.encode('utf-8')):
            errors['invalid'] = "Invalid Credentials"
        return errors

class TripManager(models.Manager):
    def trip_validation(self, postData):
        errors = {}
        if len(postData['dest']) == 0 or len(postData['desc']) == 0 or len(postData['start_date']) == 0 or len(postData['end_date']) == 0:
            errors['required'] = "All fields are required"
            return errors
        today = str(date.today())
        if postData['start_date'] <= today:
            errors['past'] = "Start Date must be a future date"
        if postData['start_date'] >= postData['end_date']:
            errors['range'] = "End Date must be after Start Date"
        return errors 

class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=60, unique=True)
    pwd_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    dest = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    planned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trips_planned")
    joined_users = models.ManyToManyField(User, related_name="trips_joined")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()