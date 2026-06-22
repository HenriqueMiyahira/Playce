from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()


class CadastroUsuarioForm(UserCreationForm):
    nome_completo = forms.CharField(
        label='Nome completo',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'autocomplete': 'name'}),
    )
    email = forms.EmailField(
        label='E-mail',
        required=True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    field_order = ['nome_completo', 'username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Usuario'
        self.fields['username'].widget.attrs.update({'autocomplete': 'username'})
        self.fields['password1'].widget.attrs.update({'autocomplete': 'new-password'})
        self.fields['password2'].widget.attrs.update({'autocomplete': 'new-password'})

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Ja existe uma conta com este e-mail.')
        return email

    def save(self, commit=True):
        usuario = super().save(commit=False)
        nome_completo = self.cleaned_data['nome_completo'].strip()
        primeiro_nome, _, sobrenome = nome_completo.partition(' ')

        usuario.first_name = primeiro_nome
        usuario.last_name = sobrenome
        usuario.email = self.cleaned_data['email']

        if commit:
            usuario.save()

        return usuario


class PerfilUsuarioForm(forms.Form):
    nome_completo = forms.CharField(
        label='Nome completo',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'autocomplete': 'name'}),
    )
    email = forms.EmailField(
        label='E-mail',
        required=True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        initial = kwargs.pop('initial', {})

        form_sem_post = not args or args[0] is None

        if user and form_sem_post:
            initial.setdefault('nome_completo', user.get_full_name() or user.username)
            initial.setdefault('email', user.email)

        super().__init__(*args, initial=initial, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        qs = User.objects.filter(email__iexact=email)

        if self.user:
            qs = qs.exclude(pk=self.user.pk)

        if qs.exists():
            raise forms.ValidationError('Ja existe outra conta com este e-mail.')

        return email

    def save(self):
        nome_completo = self.cleaned_data['nome_completo'].strip()
        primeiro_nome, _, sobrenome = nome_completo.partition(' ')

        self.user.first_name = primeiro_nome
        self.user.last_name = sobrenome
        self.user.email = self.cleaned_data['email']
        self.user.save(update_fields=['first_name', 'last_name', 'email'])

        return self.user
