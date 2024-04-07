from django import forms
from .models import rockVideo

class RockVideoForm(forms.ModelForm):
    class Meta:
        model = rockVideo
        fields = ['title', 'contact_email', 'gym_address', 'is_active', 'about', 'file']