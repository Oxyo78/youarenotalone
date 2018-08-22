from django import forms

class loginUser(forms.Form):
    """ Login acces """
    username = forms.CharField(label="Nom d'utilisateur", 
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'usernameInputControl',
                'value': '',
                'placeholder': 'ex: Paul01',
            }
        ))
    password = forms.CharField(label="Mot de passe", 
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'passwordControl',
                'value': '',
                'placeholder': 'Mot de passe',
            }
        ))

class createUser(forms.Form):
    """ Create an account """
    username = forms.CharField(label="Nom d'utilisateur",
                               max_length=30,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control',
                                       'id': 'usernameInput',
                                       'value': '',
                                       'placeholder': 'ex: Paul01',
                                   }
                               ))
    email = forms.CharField(label="Email",
                               max_length=30,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control',
                                       'id': 'emailInput',
                                       'value': '',
                                       'placeholder': 'ex: paul@example.com',
                                   }
                               ))
    password = forms.CharField(label="Mot de passe",
                               widget=forms.PasswordInput(
                                   attrs={
                                       'class': 'form-control',
                                       'id': 'passwordInput',
                                       'value': '',
                                       'placeholder': 'Mot de passe',
                                   }
                               ))
    password2 = forms.CharField(label="Répétez le mot de passe",
                               widget=forms.PasswordInput(
                                   attrs={
                                       'class': 'form-control',
                                       'id': 'password2Input',
                                       'value': '',
                                       'placeholder': 'Répétez le mot de passe',
                                   }
                               ))