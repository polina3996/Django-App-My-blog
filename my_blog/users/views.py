from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm
from my_blog.settings import DEFAULT_USER_IMAGE


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

class ProfileUser(LoginRequiredMixin, UpdateView):
    """"A class based view to show and update user's profile"""
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Профиль пользователя',
                     'default_image': DEFAULT_USER_IMAGE}

    def get_success_url(self):
        # after changing and saving an updated profile
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        # getting a profile to update - only CURRENT profile
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    """"A class based view to update user's password"""
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'
