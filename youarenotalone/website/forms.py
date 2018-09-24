from django import forms
from django.forms import ModelForm, Select
from .models import City, Interest


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
                                        'title': "La première lettre de votre nom d'utilisateur sera automatiquement en masjuscule",
                                        'data-toggle': 'tooltip'
                                   }
                               ))
    email = forms.CharField(label="Email",
                            max_length=30,
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control',
                                    'id': 'emailInput',
                                    'value': '',
                                    'placeholder': 'ex: paul@example.com'
                                }
                            ))

    city = forms.CharField(label="Ville",
                            max_length=46,
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control',
                                    'id': 'cityInput',
                                    'placeholder': 'ex: Paris',
                                    'value': '',
                                    'title': 'Actuellement, seul les villes de France sont disponible',
                                    'data-toggle': 'tooltip'
                                }
                            ))

    password = forms.CharField(label="Mot de passe",
                               widget=forms.PasswordInput(
                                   attrs={
                                       'class': 'form-control',
                                       'id': 'passwordInput',
                                       'value': '',
                                       'placeholder': 'Mot de passe',
                                       'autocomplete': 'off',
                                        'title': 'Votre mot de passe doit comporter au minimum 8 caractères et contenir au moins 1 chiffre et 1 lettre',
                                        'data-toggle': 'tooltip'
                                   }
                               ))
    password2 = forms.CharField(label="Répétez le mot de passe",
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control',
                                        'id': 'password2Input',
                                        'value': '',
                                        'placeholder': 'Répétez le mot de passe',
                                        'autocomplete': 'off',
                                        'title': 'Votre mot de passe doit comporter au minimum 8 caractères et contenir au moins 1 chiffre',
                                        'data-toggle': 'tooltip'
                                    }
                                ))

class MessageReply(forms.Form):
    """ Reply to message """
    body = forms.CharField(label="Réponse",
                           widget=forms.Textarea(
                               attrs={
                                   'class': 'form-control',
                                   'id': 'bodyReply',
                                   'value': '',
                                   'placeholder': 'Tapez votre réponse ici'
                               }
                           ))


class ComposeMessage(forms.Form):
    """ Make a new message to user """
    subject = forms.CharField(label="Sujet",
                              widget=forms.TextInput(
                                  attrs={
                                    'class': 'form-control',
                                    'id': 'subjectMessage',
                                    'value': ''
                                  }
                              ))

    bodyMessage = forms.CharField(label="Message",
                                  widget=forms.Textarea(
                                      attrs={
                                        'class': 'form-control',
                                        'id': 'bodyMessage',
                                        'value': ''
                                      }
                                  ))


class SearchPeople(forms.Form):
    """ Search form """
    def getInterest():
        return Interest.objects.values_list('id', 'interestName').order_by('interestName')

    search = forms.ChoiceField(widget=forms.Select(
                                attrs={
                                    'class': 'form-control',
                                    'id': 'searchInput'
                                }),
                            choices=getInterest,
                            label=''
                            )

class InterestAdd(forms.Form):
    """ Add an interest to the user """

    def getInterest():
        return Interest.objects.values_list('id', 'interestName').order_by('interestName')

    interestAdd = forms.ChoiceField(label="Rajouter un Intérêt",
                            widget=forms.Select(
                                attrs={
                                    'class': 'form-control',
                                    'id': 'addInteretSelect'
                                }),
                            choices=getInterest)
    
    newInterest = forms.CharField(label="Un nouvel intérêt",
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control',
                                    'id': 'interestInput',
                                    'value': '',
                                    'placeholder': 'Entrez un intérêt non listé'
                                }
                            ), required=False)


def userInterest(user):
    return user.userprofile.interestId.values_list('id', 'interestName').order_by('interestName')

class InterestDel(forms.Form):
    """ Delete an interest of the user """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(InterestDel, self).__init__(*args, **kwargs)
        user = self.user

        self.fields['interestDel'] = forms.ChoiceField(label="Supprimer un Intérêt",
                                widget=forms.Select(
                                    attrs={
                                        'class': 'form-control',
                                        'id': 'delInteretSelect'
                                    }),
                                choices=userInterest(user))