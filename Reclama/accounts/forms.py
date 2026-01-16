from django import forms
from django.contrib.auth.forms import UserCreationForm

import accounts.models as accountsmodels
import defaults.models as defaultsmodels


user_types_dict = {'customer':defaultsmodels.UserTypes.CUSTOMER,'company':defaultsmodels.UserTypes.COMPANY}



class CreateUserAccountForm(forms.ModelForm):

    password2 = forms.CharField()

    class Meta:
        model = accountsmodels.UserAccount
        fields = ['email', 'password', 'user_type','password2']


    def validate_cleaned_email(email_parameter):

        duplicated_email = accountsmodels.UserAccount.objects.filter(email=email_parameter)

        if not duplicated_email:

            email_valid = True

        else:

            valid_email = False

        return email_valid


    def validate_cleaned_password(password_parameter,password2_parameter):

        if password_parameter == password2_parameter:

            password_valid = True

        else:

            password_valid = False

        return password_valid



class CreateCustomerForm(forms.ModelForm):

    class Meta:
        model = accountsmodels.Customer
        fields = ['full_name']


    def validate_null_fields(dict_parameter):

        if user_type_parameter == user_types_dict['customer']:

            if not dict_parameter['full_name']:

                dict_parameter['full_name'] = "Undefined"

            else:
                pass

        return dict_parameter



class CreateCompanyForm(forms.ModelForm):

    class Meta:
        model = accountsmodels.Company
        fields = ['name','description','location','phone_number']


        def validate_null_fields(dict_parameter):

            if not dict_parameter['name']:

                dict_parameter['name'] = "Undefined"

            else:
                pass

            if not dict_parameter['description']:

                dict_parameter['description'] = "Undefined"

            else:
                pass

            if not dict_parameter['location']:

                dict_parameter['location'] = "Undefined"

            else:
                pass

            if not dict_parameter['phone_number']:

                dict_parameter['phone_number'] = "Undefined"

            else:
                pass

            return dict_parameter



class CreateFavoriteForm(forms.ModelForm):

    class Meta:
        model = accountsmodels.Favorites
        fields = ['user_account', 'object_id', 'object_type']