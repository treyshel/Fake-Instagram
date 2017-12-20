from django import forms
from app.models import GetImage


class ImageForm(forms.ModelForm):
    class Meta:
        model = GetImage
        fields = ('caption', 'image')
