from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from books.forms import RegisterForm, ReccomandationForm
from django.views.generic import FormView, DetailView, CreateView
from django.shortcuts import redirect, render
from books.models import Person, Reccomendation
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from books.models import Person, Rental

from models import Book
from forms import GetBookForm

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
    context_object_name = 'person'

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
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.book = Book.objects.get(pk = kwargs['pk'])
        return super(ReccomandationView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        person = Person.objects.get(pk=request.user.pk)
        Reccomendation.objects.create(by=person, book=self.book)
        return redirect(reverse('profile', kwargs={'pk':request.user.pk}))

    def get_context_data(self, **kwargs):
        context = super(ReccomandationView, self).get_context_data(**kwargs)
        #context['bookform'] = ReccomandationForm(book=self.book)
        context['book'] = self.book
        return context

class GetBookView(FormView):
    template_name = 'getbook.html'
    form_class = GetBookForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.book = Book.objects.get(pk=kwargs['pk'])
        return super(GetBookView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('persons', [None])[0]
        if not pk:
            return redirect(reverse('profile', kwargs={'pk': request.user.pk}))

        person = Person.objects.get(pk=pk)
        person.shared.remove(self.book)
        to = Person.objects.get(pk=request.user.pk)

        Rental.objects.create(by=person, to=to, book=self.book)
        return redirect(reverse('profile', kwargs={'pk': request.user.pk}))

    def get_context_data(self, **kwargs):
        context = super(GetBookView, self).get_context_data(**kwargs)
        context['bookform'] = GetBookForm(book=self.book)
        context['book'] = self.book
        return context

class AddBookView(CreateView):
    template_name = "addbook.html"
    model = Book
    fields = ['title', 'author', 'picture_url', 'description']
    success_url = '/'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AddBookView, self).dispatch(request, *args, **kwargs)

### Book sharing floow
### more info here http://www.youtube.com/watch?v=THvUDMafwkU

@login_required
def accept_decline_view(request, *args, **kwargs):
    """View used for accepting or declining rentals"""

    # authorization stuff
    rental = Rental.objects.get(pk=kwargs['pk'])
    if (rental.by.pk is not request.user.pk or
            rental.status is not Rental.PENDING_SHARE):
        return redirect(reverse('overview'))

    resolution = request.GET.get('resolution', 'decline')
    if resolution == 'accept':
        rental.status = Rental.ACCEPTED
        rental.save()
    if resolution == 'decline':
        rental.by.shared.add(rental.book)
        rental.delete()

    return redirect(reverse('profile', kwargs={'pk': request.user.pk}))

@login_required
def accept_return_view(request, *args, **kwargs):
    """View used for accepting retrun of book"""

    # authorization stuff
    rental = Rental.objects.get(pk=kwargs['pk'])
    if (rental.by.pk is not request.user.pk or
            rental.status is not Rental.ACCEPTED):
        return redirect(reverse('overview'))

    rental.by.shared.add(rental.book)
    rental.delete()

    return redirect(reverse('profile', kwargs={'pk': request.user.pk}))

@login_required
def sharing_view(request, *args, **kwargs):
    """View used for sharing or unsharing a book"""
    book = Book.objects.get(pk=kwargs['pk'])
    person = Person.objects.get(pk=request.user.pk)

    action = request.GET.get('action')
    if not action:
        return redirect(reverse('overview'))

    if action == 'share':
        person.shared.add(book)

    if action == 'unshare':
        person.shared.remove(book)

    return redirect(reverse('profile', kwargs={'pk': request.user.pk}))
    
