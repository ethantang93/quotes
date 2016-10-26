from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import bcrypt, re
from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

######################## defining the USER MANAGER#########################
class UserManager(models.Manager):
    def validateReg(self, request):
        errors = self.validate_inputs(request)

        if len(errors) > 0:
            return (False, errors)

        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

        user = self.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], pw_hash=pw_hash, birthdate= request.POST['birthdate'])

        return (True, user)

    def validateLogin(self, request):
        try:
            user = User.objects.get(email=request.POST['email'])
            # The email matched a record in the database, now test passwords
            password = request.POST['password'].encode()
            if bcrypt.hashpw(password, user.pw_hash.encode()) == user.pw_hash.encode():
                return (True, user)

        except ObjectDoesNotExist:
            pass

        return (False, ["Email/password don't match."])

    def validate_inputs(self, request):
        errors = []
        if len(request.POST['name']) < 2 or len(request.POST['alias']) < 2:
            errors.append("Please include a name or alias longer than two characters.")
        if not EMAIL_REGEX.match(request.POST['email']):
            errors.append("Please include a valid email.")
        if len(request.POST['password']) < 8 or request.POST['password'] != request.POST['confirm_pw']:
            errors.append("Passwords must match and be at least 8 characters.")
        if len(request.POST['birthdate']) < 8:
            errors.append("please input a birthdate")
        return errors


######################## defining the table#########################
class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    pw_hash = models.CharField(max_length=255)
    birthdate = models.DateField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = UserManager()



class QuoteManager(models.Manager):
    def validate(self, request):
        errors =[]
        if len(request.POST['quoted_by']) < 3:
            errors.append("please input length longer than 3 characters")
        if len(request.POST['message']) < 10:
            errors.append("please input message longer than 10 characters")
        return errors
    def addquote(self, request):
        errors = self.validate(request)
        if len(errors) >0:
            return (False, errors)
        user = User.objects.get(id=request.session['user']['id'])
        quote = self.create(quoted_by=request.POST['quoted_by'], message=request.POST['message'], created_by=user)
        return (True, quote)
    def addFavorite(self,quote_id,user_id):
        self.get(id=quote_id).liked_by.add(User.objects.get(id=user_id))
    def removeFavorite(self, quote_id, user_id):
        self.get(id=quote_id).liked_by.remove(User.objects.get(id=user_id))
        



class Quote(models.Model):
    quoted_by = models.CharField(max_length=100)
    message = models.CharField(max_length=500)
    created_by = models.ForeignKey(User)
    liked_by = models.ManyToManyField(User, related_name="liked_quote")

    objects = QuoteManager()
