from django import forms

class SignIn_Form(forms.Form):
    username = forms.CharField(min_length=4, max_length=20)
    pass1 = forms.CharField(min_length=6, max_length=16)

class SignUp_Form(forms.Form):
    username = forms.CharField(min_length=4, max_length=20)
    fname = forms.CharField(min_length=1, max_length=20)
    lname = forms.CharField(min_length=1, max_length=20)
    email = forms.EmailField(max_length=50)
    pass1 = forms.CharField(min_length=6, max_length=16)
    pass2 = forms.CharField(min_length=6, max_length=16)
