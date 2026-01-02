from django import forms
from django.contrib.auth.forms import UserCreationForm
import accounts.models as accountsmodels


class ChooseUserTypeForm(forms.Form):
    user_type = serializers.PositiveSmallIntegerField()


class CreateUserForm(forms.Form):
    #USER
    username = serializers.CharField(max_length=30)
    email = serializers.EmailField(max_length=60)
    password1 = serializers.TextField()
    password2  = serializers.TextField()


class CreateCustomerProfileForm(forms.Form):

    name = models.CharField(max_length=60,blank=True,default='Undefined Name')


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
