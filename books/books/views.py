
from django.views.generic import TemplateView, DetailView
from models import Book

class Overview(TemplateView):
    template_name = 'overview.html'

class BookView(DetailView):
    template_name = 'book.html'
    model = Book
    context_object_name = 'book'

