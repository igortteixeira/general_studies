from django import forms
from .models import ComplaintPost,ComplaintComment



class CreateComplaintForm(forms.ModelForm):

    class Meta:
        model = ComplaintPost
        fields = ['title','body']



class UpdateComplaintForm(forms.ModelForm):

    class Meta:
        model = ComplaintPost
        fields = ['body']


class CloseComplaintForm(forms.ModelForm):

    class Meta:
        model = ComplaintPost
        fields = ['score_type','is_solved']


class CreateCommentForm(forms.ModelForm):

    class Meta:
        model = ComplaintComment
        fields = ['body']


class UpdateCommentForm(forms.ModelForm):

    class Meta:
        model = ComplaintComment
        fields = ['body']
