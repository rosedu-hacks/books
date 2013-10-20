from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from models import Person

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


