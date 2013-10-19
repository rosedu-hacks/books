from django.contrib.auth.forms import UserCreationForm
from models import Person

class LoginForm(UserCreationForm):
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

