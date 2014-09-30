from django import forms
from chain_of_command import models
from ckeditor.widgets import CKEditorWidget

__author__ = 'awhite'


class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        exclude = ['id', 'P', 'M']


class PostForm(forms.ModelForm):
    Content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = models.Post
        exclude = ['id', 'Creator', 'timestamp']


class PositionForm(forms.ModelForm):
    class Meta:
        models = models.Position
        exclude = ['id']


class OrganizationForm(forms.ModelForm):
    Description = forms.CharField(widget=CKEditorWidget())
    MemberName = forms.CharField(max_length=80)

    class Meta:
        model = models.Organization
        exclude = ['id']


class Org_applicationForm(forms.ModelForm):
    member_name = forms.CharField(80)

    class Meta:
        model = models.Member
        exclude = ['id', 'User', 'Provisional', 'Name']