from django import forms
from django.contrib.auth.forms import UserCreationForm
from models import Office, ProjectDetail, MunicipalityDetail
from django.contrib.auth.models import User
class OfficeForm(forms.ModelForm):
    class Meta:
        model = Office
        exclude = ()

class OfficeEditForm(forms.ModelForm):
    class Meta:
        model = Office
        exclude = ('is_project', 'is_municipality')

class UserForm(UserCreationForm):
    
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
   
    password1 = forms.CharField(initial='sa2das33@dsErZZasd')
    password2 = forms.CharField(initial='sa2das33@dsErZZasd')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ProjectDetailForm(forms.ModelForm):
    class Meta:
        model = ProjectDetail
        exclude = ('office',)

class MunicipalityDetailForm(forms.ModelForm):
    class Meta:
        model = MunicipalityDetail
        exclude = ('office', )
