from django import forms

from . import models

class EditProfile(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        
        
    class Meta:
        model = models.User
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_picture', ]