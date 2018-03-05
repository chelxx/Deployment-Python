# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.messages import error
from datetime import datetime
from .models import *
import bcrypt
import re

# Create your views here.
def index(request):
    print ('THERE ARE NO MISTAKES HERE, JUST HAPPY LITTLE ACCIDENTS. WOMP WOMP!') #I LIED THIS IS MISTAKE ISLAND :(
    return render(request, 'belt_app/index.html')

def register(request):
    print ('REGISTER VIEW')
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        print ('IF - REGISTER')
        for error in errors:
            messages.error(request, error)
        return redirect('/')
    else:
        print ('ELSE - REGISTER')
        user = User.objects.create(
            first = request.POST['first'],
            last = request.POST['last'],
            alias = request.POST['alias'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()),
            birthday = request.POST['birthday'],
        ) 
        request.session['user_id'] = user.id
        return redirect('/success')

def login(request):
    print('LOGIN VIEW')
    errors = []
    try:
        print ('TRY - LOGIN')
        u = User.objects.get(email=request.POST['email'])
        if bcrypt.checkpw(request.POST['password'].encode(), (User.objects.filter(email=request.POST['email']))[0].password.encode()) == True:  
            request.session['user_id'] = u.id 
            user = User.objects.get(id=u.id)
            return redirect('/success')
        else:
            errors.append('Invalid Password!')
    except:
        print ('EXCEPT - LOGIN')
        errors.append('Email does not exist!')
    for error in errors:
        messages.error(request, error)
    return redirect('/')   


def logout(request):
    print('LOGOUT VIEW')
    errors = []
    try:
        print ('TRY LOGOUT')
        del request.session['user_id']
        request.session.clear()
        errors.append('You have been logged out! Bye, dude!')
    except KeyError:
        print ('EXCEPT LOGOUT')
        pass    
    for error in errors:
        messages.error(request, error)
    return redirect('/')

#BELT EXAM VIEWS START HERE:
def success(request):
    print('SUCCESS VIEW')
    user = User.objects.get(id=request.session['user_id'])
    friends = Friend.objects.filter(friender=user)
    all_users = User.objects.all()
    my_friends = []
    for person in friends:
        print('I DID MY BEST!!!')
        my_friends.append(person.friendee)
    context = {
        'user' : user,
        'all_users' : all_users,
        'my_friends' : my_friends,
    }
    return render(request, 'belt_app/success.html', context)

def friend(request, id):
    print('FRIENDING... :)')
    User.objects.YesToFriendship(request.session['user_id'], id)
    return redirect('/success')

def unfriend(request, id):
    print('UNFRIENDING... :(')
    User.objects.NoToFriendship(request.session['user_id'], id)
    return redirect('/success')

def profile(request, id):
    print('PROFILE VIEW')
    user = User.objects.get(id=id)
    context = {
        'user' : user,
    }
    return render(request, 'belt_app/profile.html', context)