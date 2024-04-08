from django import forms

class ResumeUploadForm(forms.Form):
    resume = forms.FileField(label='Upload Your Resume', widget=forms.ClearableFileInput(attrs={'multiple':False}), required=True)
