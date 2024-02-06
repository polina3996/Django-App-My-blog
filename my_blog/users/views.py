from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from .forms import LoginUserForm, RegisterUserForm


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


class RegisterUser(CreateView):
    """"A class based view to register"""
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')

# def register(request):
#     if request.method == 'POST':
#         # sending the filled form
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             # create a new user without adding him to database
#             user = form.save(commit=False)
#             # encrypting inputted password
#             user.set_password(form.cleaned_data['password'])
#             # user is saved to database
#             user.save()
#             return render(request, 'users/register_done.html')
#     else:
#         # GET-request -> empty form
#         form = RegisterUserForm()
#     return render(request, 'users/register.html', {'form': form})
