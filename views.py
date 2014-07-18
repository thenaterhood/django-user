from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from user.forms import *  # all forms
from user.models import *

import urllib
import hashlib
import json

# Create your views here.

@login_required
def settings_dashboard(request):
  pageData = {}
  pageData['user'] = request.user
  return render_to_response("user_settings.html", pageData)

def register_user(request):
    """
    Defines the request to response of the user registration page

    Returns:
            either the same page or a rendered page of register.html
    """
    args = {}
    args['form'] = UserRegistrationForm()

    # see if the method of the request objerct 'POST' -> first time it should
    # be no, second time yes
    if request.method == 'POST':
        # pass the values from POST dictionary into the MyRegistrationForm and
        # create form object
        form = UserRegistrationForm(request.POST)

        if form.is_valid():  # is the form valid (info is correct)
            # save the form, save the registration information for the new user
            user = form.save(commit=False)

            if (User.objects.filter(username=user.username).count() < 1):

                user.save()
                return HttpResponseRedirect('/user/login/')

            else:
                messages.error(
                    request, "Sorry, that username is already taken.")
                args['form'] = UserRegistrationForm(request.POST)

        else:
            args['form'] = UserRegistrationForm(request.POST)
            messages.error(
                request, "You didn't fill out the form correctly! Please check your input.")

    # what happens the first time the user visits the register page

    args.update(csrf(request))  # pass through the csrf token

    # pass the form to the register.html template
    return render_to_response('user_register.html', RequestContext(request, args))


def login_user(request):
    """
    Defines the request to response of the functionality of login

    Returns:
            A rendered page of login.html
    """

    c = {}

    return render_to_response('user_login.html', RequestContext(request, c))


def auth_user(request):
    """
    Defines an intermediate step/page that checks the validity of a user

    Returns:
            A redirect to the loggin success page or the user invalid page
    """

    # blank string means if you can't find a value, use a blank string
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    # assigns a user obj to 'user' if it exists, otherwise return 'None'
    user = auth.authenticate(username=username, password=password)

    if user is not None:  # if we found a user that authenticates
        auth.login(request, user)  # signify the user as logged in
        # redirect them to the loggedin page
        return HttpResponseRedirect('/user/welcome')
    else:
        messages.error(request, "Invalid Login.")
        # redirect them to the invalid login page
        return HttpResponseRedirect('/user/login')


@login_required
def welcome(request):

    return render_to_response('user_welcome.html', {'user': request.user})


def logout(request):
    """
    Defines the request to response of logout page returning back to the
    login page

    Returns:
            A rendered page of login.html
    """
    c = {}
    c.update(csrf(request))
    messages.info(request, "You are now logged out.")
    auth.logout(request)  # use auth to logout the user
    return render_to_response('user_login.html', RequestContext(request, c))


def _build_gravatar_url(user, size=40):
    email = user.email

    # construct the url
    gravatar_url = "http://www.gravatar.com/avatar/" + \
        hashlib.md5(email.lower().encode("UTF-8")).hexdigest() + "?"
    gravatar_url += urllib.parse.urlencode({'s': str(size)})

    return gravatar_url


def _get_gravatar_profile(user):
    email = user.email

    gravatar_url = "http://www.gravatar.com/" + \
        hashlib.md5(email.lower().encode("UTF-8")).hexdigest() + ".json"

    try:
        profileHandle = urllib.request.urlopen(
            gravatar_url, timeout=5).read().decode("UTF-8")

        profileData = json.loads(profileHandle)

    except:
        profileData = {}

    return profileData


def view_profile(request, username):

    pageData = {}
    pageData['request_user'] = request.user

    pageData['anonymous'] = (
        request.user.__class__.__name__ == "AnonymousUser")

    try:
        user = User.objects.get(username=username)

        pageData['gravatar_url'] = _build_gravatar_url(user, 200)
        pageData['gravatar_profile'] = _get_gravatar_profile(user)
    except:
        pageData['nouser'] = True
        user = None

    pageData['user_profile'] = user

    return render_to_response('user_profile.html', RequestContext(request, pageData))


@login_required
def change_password(request):
    pageData = {}

    if (request.method == 'POST'):
        form = PasswordForm(request.POST)

        if (form.is_valid() and request.user.check_password(form.cleaned_data['password0'])):

            request.user.set_password(form.cleaned_data['password1'])
            request.user.save()

            messages.info(request, "Password updated successfully!")
            return HttpResponseRedirect('/user/profile/' + request.user.username)

        else:

            messages.error(
                request, "Sorry, one of your inputs wasn't quite right. Give it another go.")

    pageData['form'] = PasswordForm()

    return render_to_response('user_password.html', RequestContext(request, pageData))


@login_required
def edit_profile(request):

    pageData = {}

    if (request.method == 'POST'):
        form = EditUserForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()

            messages.info(request, "Your profile was updated.")

            return HttpResponseRedirect('/user/profile/' + request.user.username)

        else:

            messages.error(
                request, "Something wasn't quite right, give it another go.")

            pageData['form'] = EditUserForm(request.POST)

            return HttpResponseRedirect('/user/profile/' + request.user.username)

    else:
        pageData['form'] = EditUserForm(instance=request.user)

    return render_to_response('user_edit.html', RequestContext(request, pageData))

def about_app(request):
    """
    Optional method with an about page and
    documentation for this application
    """
    pageData = {}
    pageData['user'] = request.user
    return render_to_response('user_aboutapp.html', RequestContext(request, pageData))
