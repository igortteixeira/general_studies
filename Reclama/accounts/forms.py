from django import forms
from django.contrib.auth.forms import UserCreationForm
import accounts.models as accountsmodels




class ChooseUserTypeForm(forms.ModelForm):
    class Meta:
        model = accountsmodels.CustomUser
        fields = ['user_type']


class CreateUserForm(UserCreationForm):

    class Meta:
        model = accountsmodels.CustomUser
        fields = ['username', 'password1', 'password2']


class CreateCustomerProfileForm(forms.ModelForm):

    class Meta:
        model = accountsmodels.CustomerProfile
        fields = ['name','profile_image']


class UpdateCustomerProfileForm(forms.ModelForm):
    class Meta:
        model = accountsmodels.CustomerProfile
        fields = ['name','profile_image']


class CreateCompanyProfileForm(forms.ModelForm):

    class Meta:
        model = accountsmodels.CompanyProfile
        fields = ['name','description','location','phone_number','profile_image']



class UpdateCompanyProfileForm(forms.ModelForm):
    class Meta:
        model = accountsmodels.CompanyProfile
        fields = ['name','description','location','phone_number','profile_image']
