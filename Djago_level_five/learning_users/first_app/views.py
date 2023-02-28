from django.shortcuts import render
from first_app.forms import UserForm, UserProfileForm
# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'index.html')


def registartion(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        print(f"request data is {request.FILES}")

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            print(f"User data {user}")
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, "registration.html", context={'user_form': user_form, 'profile_form': profile_form,
                                                         'registered': registered})


def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponse("Account is not active")
        else:
            print("Username and password is incorrect")
            return HttpResponse("Invalid username and password")
    else:
        return render(request, 'login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))