from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

def index(request):
	return render(request, 'pokes/index.html')

def flashErrors(request, errors):
	for error in errors:
		messages.error(request, errors[error])

def currentUser(request):
	id = request.session['user_id']
	return User.objects.get(id=id)

def pokes(request):
	if 'user_id' in request.session:
		current_user = currentUser(request)
		# my_pokes = current_user.pokes.all()
		other_users = User.objects.exclude(id=current_user.id)

		context = {
			'current_user': current_user, 
			# 'my_pokes': my_pokes, 
			'other_users': other_users
		}
		return render(request, 'pokes/pokes.html', context)  #method to display pokes page
	return redirect('/')





def add_poke(request, id):
	if request.method == 'POST':
		current_user = currentUser(request)
		# current_user.pokes = current_user.pokes + 1
		# current_user.save()
		poke_user = User.objects.get(id=id)
		poke_user.pokes = poke_user.pokes + 1
		poke_user.save()
		
		print '*****poke****'
		print poke_user.pokes
		return redirect('/pokes')





def register(request):
	if request.method == 'POST':
		errors = User.objects.validateRegister(request.POST)
		if not errors:
			user = User.objects.createUser(request.POST)
			request.session['user_id'] = user.id
			return redirect('/pokes')

		flashErrors(request, errors)
	return redirect('/')

def login(request):
	if request.method == 'POST':
		errors = User.objects.validateLogin(request.POST)

	if not errors:
		user = User.objects.filter(email=request.POST['email']).first()
		if user:
			password = str(request.POST['password'])
			user_pasword = str(user.password)
			hashed_pw = bcrypt.hashpw(password, user_pasword)

			if hashed_pw == user.password:
				request.session['user_id'] = user.id
				return redirect('/pokes')

			errors['password'] = 'Invalid account information'
	flashErrors(request, errors)		
	return redirect('/pokes')

def logout(request):
	if 'user_id' in request.session:
		request.session.pop('user_id')
	return redirect('/')