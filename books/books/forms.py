from django.contrib.auth.forms import UserCreationForm
from models import Person, Book, Tag
from django import forms
from django.forms.widgets import Textarea
from django.forms.extras.widgets import SelectDateWidget

class RegisterForm(UserCreationForm):
    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'email')

    def save(self):
        password = self.cleaned_data.pop('password1')
        self.cleaned_data.pop('password2')

        person = Person(**self.cleaned_data)
        person.set_password(password)
        person.save()
        return person

class ReccomandationForm(forms.Form):
    
    description = forms.CharField(widget = Textarea())
    def __init__(self, *args, **kwargs):
        super(ReccomandationForm, self).__init__(*args, **kwargs)

class GetBookForm(forms.Form):
    return_date = forms.DateField(widget=SelectDateWidget)

    def __init__(self, *args, **kwargs):
        if 'book' not in kwargs:
            return

        self.book = kwargs.pop('book')
        super(GetBookForm, self).__init__(*args, **kwargs)
        shared_by = self.book.shared_by.all()
        self.fields['persons'] = forms.ChoiceField(widget=forms.Select,
                                                   choices=[(u.pk, u.name) for u in shared_by])

class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['tags'] = forms.MultipleChoiceField(choices = [(t.id, t.name) for t in Tag.objects.all()],
                                                        required=False,
                                                        widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Book
        fields = ['title', 'author', 'picture_url', 'description']

    def save(self, *args, **kwargs):
        book = super(BookForm, self).save(*args, **kwargs)
        tags = Tag.objects.filter(pk__in=self.cleaned_data['tags'])
        for tag in tags:
            book.tags.add(tag)

        return book
    
