from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from books.forms import LoginForm
from django.views.generic import FormView, DetailView
from django.shortcuts import redirect, render
from books.models import Person

class Overview(TemplateView):
    template_name = 'overview.html'

class Register(FormView):
    template_name = 'register.html'
    form_class = LoginForm
    
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password2']
            user = form.save()
            username = user.username
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('profile', user.pk)
        return render(request, self.template_name, {'form': form})

class Profile(DetailView):
    template_name = 'profile.html'
    model = Person

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        return context

