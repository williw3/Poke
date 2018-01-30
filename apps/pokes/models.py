from __future__ import unicode_literals
from django.db import models
import datetime
import re
import bcrypt


NAME_REGEX = re.compile(r"^[-a-zA-Z']+$")
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
	def validateLogin(self, postData):
		errors = {}
		if len(postData['email']) < 3:
			errors['email'] = 'Must enter an email.'
		if len(postData['password']) < 8:
			errors['password'] = 'Password must contain at least 8 characters'
		return errors

	def validateRegister(self, postData):
		errors = {}
		birth_date = datetime.datetime.strptime(postData['birthday'], '%Y-%m-%d').date()
		today_date = datetime.date.today()

		if len(postData['name']) < 1:
			errors['name'] = 'Must enter a name'
		elif not NAME_REGEX.match(postData['name']):
			errors['name'] = 'name contains invalid characters'
		if len(postData['alias']) < 1:
			errors['alias'] = 'Must enter an alias'
		if self.filter(alias=postData['alias']):
			errors['alias'] ='alias already in use'
		if len(postData['email']) < 1:
			errors['email'] = 'Must enter an email'
		elif not EMAIL_REGEX.match(postData['email']):
			errors['email'] = 'Must enter valid email'
		if self.filter(email=postData['email']):
			errors['email'] = 'email already in use'
		if len(postData['password']) < 8:
			errors['password'] = 'Password must contain at least 8 characters'
		elif not postData['password'] == postData['password_confirm']:
			errors['password'] = 'Passwords do not match'
		if birth_date >= today_date:
			errors['birthday'] = 'Must enter a valid DOB'
		return errors

	def createUser(self, postData):
		password = str(postData['password'])
		hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())
		user = self.create(
			name=postData['name'], 
			alias=postData['alias'],
			email=postData['email'], 
			password=hashed_pw,
			birthday=postData['birthday']
			)

		return user

class User(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	birthday = models.DateField()
	pokes = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class PokeManager(models.Manager):
	def pokeAdd(self, postData, user):
		poke = self.create(
			user=user
			)
		user.pokers.add(poke)
		return poke

class Poke(models.Model):
	poked_by =models.ManyToManyField(User, related_name='pokers')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = PokeManager()





