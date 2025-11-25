from django import forms
import complaints.models as complaintsmodels


class CreateComplaintForm(forms.ModelForm):

    class Meta:
        model = complaintsmodels.ComplaintPost
        fields = ['title','body']



class UpdateComplaintForm(forms.ModelForm):

    class Meta:
        model = complaintsmodels.ComplaintPost
        fields = ['body']


class CloseComplaintForm(forms.ModelForm):

    class Meta:
        model = complaintsmodels.ComplaintPost
        fields = ['score_type','is_solved']


class CreateCommentForm(forms.ModelForm):

    class Meta:
        model = complaintsmodels.ComplaintComment
        fields = ['body']


class UpdateCommentForm(forms.ModelForm):

    class Meta:
        model =complaintsmodels.ComplaintComment
        fields = ['body']
