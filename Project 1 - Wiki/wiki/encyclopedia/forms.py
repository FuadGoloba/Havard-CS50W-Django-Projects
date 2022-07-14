from django import forms


class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'style':'width: 300px;', 'class':'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":50, 'class':'form-control'}))
    
    def clean_title(self):
        data = self.cleaned_data['title']
        return data
    
    def clean_content(self):
        data = self.cleaned_data['content']
        return data
    
class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":50, 'class':'form-control'}))
    
    
