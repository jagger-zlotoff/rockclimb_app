from django import forms
from django.core.exceptions import ValidationError
from .models import rockVideo

class RockVideoForm(forms.ModelForm):
    class Meta:
        model = rockVideo
        fields = ['title', 'contact_email', 'gym_name', 'gym_address', 'is_active', 'about', 'file', 'image']
    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get("file")
        image = cleaned_data.get("image")

        if not file and not image:
            raise ValidationError("You must upload either a video or an image.")

        if file and image:
            raise ValidationError("Please upload only a video or an image, not both.")

        return cleaned_data