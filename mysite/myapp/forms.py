from django import forms

class ConnectForm(forms.Form):
    username = forms.CharField(label='Votre Nom', max_length=30, widget=forms.TextInput(
            attrs={'placeholder': 'Nom du boy'}
    ))
    password = forms.CharField(label='Password', max_length=16, widget=forms.PasswordInput(
        attrs={'placeholder': 'Mot de passe du boy'}
    ))
    pass

class NewUserForm(forms.Form):
    username =  forms.CharField(label='Votre Nom', max_length=30, widget=forms.TextInput(
            attrs={'placeholder': 'Nom utilisateur'}
    ))
    password = forms.CharField(label='Password', max_length=16, widget=forms.PasswordInput(
        attrs={'placeholder': 'Mot de passe'}
    ))
    password_2 = forms.CharField(label='Password', max_length=16, widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirmer Mot de passe'}
    ))
    pass

class CreateTicketForm(forms.Form):
    pass

class CreateReviewForm(forms.Form):
    pass

class SubscriptionForm(forms.Form):
    pass

