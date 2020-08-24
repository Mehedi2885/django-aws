from django.shortcuts import render, redirect
from django.views import View
from .forms import UserCreationForm, UserLoginForm
from django.contrib.auth import login, get_user_model, logout

# Create your views here.

User = get_user_model()


class UserCreateRegister(View):
    template_name = 'accounts/register_create.html'
    form = UserCreationForm()

    def get(self, request, *args, **kwargs):
        context = {'form': self.form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            form = self.form
        context = {'form': form}
        return render(request, self.template_name, context)


class UserLoginCBV(View):
    template_name = 'accounts/login_form.html'
    form = UserLoginForm()

    def get(self, request, *args, **kwargs):
        context = {'form': self.form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user_obj = form.cleaned_data.get('user_obj')
            #user_obj = User.objects.get(username__iexact=username_form)
            login(request, user_obj)
            return redirect('/admin/')
        context = {'form': form}
        return render(request, self.template_name, context)


class UserLogout(View):

    def get(self, request):
        logout(request)
        return redirect('/admin/')