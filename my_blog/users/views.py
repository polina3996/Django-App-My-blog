from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import LoginUserForm


# Create your views here.
class LoginUser(LoginView):
    """"A class based view to log in for non-authorized users"""
    # or simply AuthenticationForm(works together with LoginView)
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}


    # if request.method == 'POST':
    #     # sending the filled form
    #     form = LoginUserForm(request.POST)
    #     if form.is_valid():
    #         # authentication - search in the database
    #         user = authenticate(request,
    #                             username=form.cleaned_data['username'],
    #                             password=form.cleaned_data['password'])
    #         if user and user.is_active:
    #             # user exists and is not banned -> authorization
    #             login(request, user)
    #             # redirection to his profile + writing him down into session
    #             return HttpResponseRedirect(reverse('users:profile'))
    # else:
    #     # GET-request -> empty form
    #     form = LoginUserForm()
    # return render(request, 'users/login.html', {'form': form})


def logout_user(request):
    """A view to log out for authorized users"""
    # logging out and redirection to log in
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))
