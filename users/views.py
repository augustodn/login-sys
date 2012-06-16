from django.core.mail import send_mail
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from users.models import User
from users.forms import UserForm

# Hashing functions.

import random
import string
import hashlib

SALT_LEN = 11

def combine(salt, password):
    mini_hash = hashlib.sha256(password + salt).hexdigest()
    h = mini_hash[:len(password)] + salt + mini_hash[len(password):]
    return h

def make(password):
    salt = ''.join(random.choice(string.hexdigits[:-6])\
        for x in xrange(SALT_LEN))
    return combine(salt, password)

def valid(h, password):
    salt = h[len(password):len(password)+SALT_LEN]
    return h == combine(salt, password)


# Create your views here.

def login(request):
    template = 'users/login.html'
    content = {}
    context_instance=RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        content['username'] = username
        try:
            u = User.objects.get(username=username)

            if valid(u.password, request.POST['password']):
                cookie_val = make(u.username)
                response = HttpResponseRedirect('/users/welcome/?u=%s' \
                    %username)
                response.set_cookie('user_id',cookie_val)
                return response
            else:
                content['error_message'] = 'Bad Password'

        except User.DoesNotExist:
            content['error_message'] = 'Bad Username'

    return render_to_response(template, content, context_instance)

def signup(request):
    template = 'users/signup.html'
    context_instance = RequestContext(request)

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            #Encript password before save it in the DB
            new_user.password = make(new_user.password)
            new_user.save()
            return HttpResponseRedirect('/users/login/')
    else:
        form = UserForm()

    return render_to_response(template, {'form': form}, context_instance)

def welcome(request):
    try:
        username = request.GET['u']
        cookie = request.COOKIES['user_id']
    except KeyError:
        return HttpResponseRedirect('/users/login/')

    if valid(cookie, username):
        return HttpResponse('<h2>Welcome, %s!' % username)
    else:
        return HttpResponseRedirect('/users/logout/')

def logout(request):
    response = HttpResponseRedirect('/users/login/')
    response.delete_cookie('user_id')
    return response

def recover(request):
    template = 'users/recover.html'
    context_instance = RequestContext(request)
    recover_message = 'This is a foo message'
    content = {}

    if request.method == 'POST':
        email = request.POST['email']
        content['email'] = email
        try:
            u = User.objects.get(email=email)
            send_mail(
                'Recover your password',
                recover_message,
                'noreply@localhost',
                [u.email],
            )

            return HttpResponseRedirect('/users/login/')
        except User.DoesNotExist:
            content['error_message'] = "E-mail address doesn't exist"

    return render_to_response(template, content, context_instance)
"""
def newpassword(request):
    #mail validation and reset password
    pass
"""
