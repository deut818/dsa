from django import forms

class ContactForm(forms.Form):
    fname = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    lname = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'class':'form-control'}), required=False)
    subject = forms.CharField(label='Subiect', widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    message = forms.CharField(label='Message', widget=forms.Textarea(attrs={'class':'form-control'}), required=False)
