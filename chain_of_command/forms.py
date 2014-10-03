from django import forms
from django.forms.utils import ErrorList
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
    def __init__(self, org_id, data=None, files=None, auto_id='id_%s',
                 prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=None,
                 empty_permitted=False, instance=None):
        super().__init__(data, files, auto_id, prefix, initial, error_class,
                         label_suffix, empty_permitted, instance)
        self.fields["associated"].queryset = models.Member.objects.filter(
            Organization_id=org_id)
        self.fields['boss'].queryset = models.Position.objects.filter(
            Organization_id=org_id)

    class Meta:
        model = models.Position
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