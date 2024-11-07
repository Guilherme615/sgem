from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Produto, MovimentoEstoque, Pedido, Escola

# Formulário de Login
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# Formulário de Registro
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu e-mail'
        })
    )

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Nome de Usuário"
    )

    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        label="Nome"
    )

    escola = forms.ModelChoiceField(
        queryset=Escola.objects.all(), 
        required=True, 
        widget=forms.Select(attrs={'class': 'form-control'}))


    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'password1', 'password2', 'escola')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está em uso.')
        return email

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Nome de Usuário"
    )

    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        label="Nome"
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está em uso.')
        return email

# Formulário para Cadastro de Produtos
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'categoria', 'quantidade', 'data_validade']
        widgets = {
            'data_validade': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

# Formulário para Movimentação de Estoque (Entrada e Saída)
class MovimentoEstoqueForm(forms.ModelForm):
    class Meta:
        model = MovimentoEstoque
        fields = ['produto', 'tipo', 'quantidade']
        widgets = {
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'nota_fiscal': forms.TextInput(attrs={'class': 'form-control'}),
            'destino': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Formulário para Cadastro de Usuários (Admin)
class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super(UsuarioForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['produto', 'quantidade']

class EscolaForm(forms.ModelForm):
    class Meta:
        model = Escola
        fields = ['nome']  # Apenas o campo 'nome' será exibido no formulário
