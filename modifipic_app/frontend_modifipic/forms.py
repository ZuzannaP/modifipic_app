from django import forms
from img_modifier.models import TheImage


class ImageFileUploadForm(forms.ModelForm):
    class Meta:
        model = TheImage
        fields = ('file',)
