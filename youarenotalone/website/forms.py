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

    # def getCity():
    #     return City.objects.values_list('id', 'cityName').order_by('cityName')
    #     # return City.objects.values_list('id', 'cityName').order_by('cityName').distinct('cityName') => Doesn't work with sqlite3

    # city = forms.ChoiceField(label="Ville ",
    #                         widget=forms.Select(
    #                             attrs={
    #                                 'class': 'form-control',
    #                                 'id': 'citySelect'
    #                             }),
    #                         choices=getCity
    #                         )
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
    search = forms.CharField(label="",
                             widget=forms.TextInput(
                                 attrs={
                                     'class': 'form-control',
                                     'id': 'searchInput',
                                     'value': '',
                                     'placeholder': 'Commencez votre recherche ici'
                                 }
                             ))

class InterestAdd(forms.Form):
    """ Add an interest to the user """

    def getInterest():
        return Interest.objects.values_list('id', 'interestName').order_by('interestName')
        # return City.objects.values_list('id', 'cityName').order_by('cityName').distinct('cityName') => Doesn't work with sqlite3

    interestAdd = forms.ChoiceField(label="Rajouter un Intérêt",
                            widget=forms.Select(
                                attrs={
                                    'class': 'form-control',
                                    'id': 'addInteretSelect'
                                }),
                            choices=getInterest
                            )
    
    newInterest = forms.CharField(label="Un nouvel intérêt",
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control',
                                    'id': 'interestInput',
                                    'value': '',
                                    'placeholder': 'Entrez un intérêt non listé'
                                }
                            ), required=False)


class InterestDel(forms.Form):
    """ Delete an interest to the user """

    def getInterest():
        return Interest.objects.values_list('id', 'interestName').order_by('interestName')
        # return City.objects.values_list('id', 'cityName').order_by('cityName').distinct('cityName') => Doesn't work with sqlite3

    interestDel = forms.ChoiceField(label="Supprimer un Intérêt",
                            widget=forms.Select(
                                attrs={
                                    'class': 'form-control',
                                    'id': 'delInteretSelect'
                                }),
                            choices=getInterest
                            )
