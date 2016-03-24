from django import forms
from upload.models import Collection

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        exclude = ['user']
