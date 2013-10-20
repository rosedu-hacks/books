from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from books.forms import RegisterForm, ReccomandationForm
from django.views.generic import FormView, DetailView
from django.shortcuts import redirect, render
from books.models import Person, Reccomendation
from django.core.urlresolvers import reverse
from models import Book

class Overview(TemplateView):
    template_name = 'overview.html'

class Register(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    
    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password2']
            user = form.save()
            username = user.username
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('overview')
        return render(request, self.template_name, {'form': form})

class Profile(DetailView):
    template_name = 'profile.html'
    model = Person

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        return context

class BookView(DetailView):
    template_name = 'book.html'
    model = Book
    context_object_name = 'book'

class ReccomandationView(FormView):
    template_name = 'recc.html'
    model = Reccomendation
    form_class = ReccomandationForm
    
    def dispatch(self, request, *args, **kwargs):
        self.book = Book.ojects.get(pk = kwargs['pk'])
        return super(ReccomandationView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        person = Person.objects.get(pk=request.user.pk)
        Reccomendation.objects.create(by=person, book=self.book)
        return redirect('/')

    def get_context_data(self, **kwargs):
        return super(ReccomandationView, self).get_context_data(**kwargs)

