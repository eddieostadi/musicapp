from django import forms
from django.forms import TextInput

from .models import Student, Song


class LoginForm(forms.Form):
    username = forms.CharField(empty_value=False, label='username', max_length=30)
    password = forms.CharField(empty_value=False, label='password', max_length=25, widget=forms.PasswordInput)


class NewUserForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['email', 'username', 'password']

    password2 = forms.CharField(label='repeat password', required=True)

    def valid_password(self):
        if self.cleaned_data["password"] == self.data["password2"]:
            user = super(NewUserForm, self).save(commit=False)

            return True
        else:

            return False


class NewSongForm(forms.ModelForm):
    class Meta:
        model = Song
        # model.sender= Student.objects.get(pk=id)
        fields = ['title', 'artist', 'year', 'url', 'image']
        # widgets = {
        #     'likedBy': TextInput(attrs={'readonly': 'readonly'})
        # }


class QueryForm(forms.ModelForm):
    class Meta:
        model = Song
        # model.sender= Student.objects.get(pk=id)
        fields = ['title', 'artist', 'year']

class Qform(forms.Form):
    title= forms.CharField(max_length=30, required=False, label="Title")
    year= forms.IntegerField(required=False, label="Year")
    artist = forms.CharField(max_length=30, required=False, label="Artist")