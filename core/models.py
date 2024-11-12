from django.db import models
from django.contrib.auth.models import User

# Modelo para Categorias de Produtos (Ex: Alimentos, Bebidas)
class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    escola = models.ForeignKey('Escola', on_delete=models.CASCADE, null=True, blank=True)  # Permitindo nulos por enquanto

    def __str__(self):
        return self.nome

class Escola(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

# Modelo para Produtos
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    data_validade = models.DateField()
    is_deleted = models.BooleanField(default=False)  # Campo para marcar produtos excluídos

    def __str__(self):
        return self.nome

# Modelo para Registro de Entrada e Saída de Produtos no Estoque
class MovimentoEstoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=[('entrada', 'Entrada'), ('saida', 'Saída')])
    quantidade = models.IntegerField()
    data_movimento = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.tipo} - {self.produto.nome} ({self.quantidade})'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=[
        ('diretor', 'Diretor'),
        ('nutricionista', 'Nutricionista'),
        ('adm', 'Administrador')
    ], default='adm')
    escola = models.ForeignKey('Escola', on_delete=models.SET_NULL, null=True, blank=True)  # Adiciona a chave estrangeira para associar o usuário à escola


    def __str__(self):
        return self.user.username
    

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Adiciona a relação com o usuário
    produto = models.CharField(max_length=100)  # Exemplo de campo para o produto
    quantidade = models.PositiveIntegerField()  # Campo para quantidade
    status = models.CharField(max_length=20, choices=[
        ('Pendente', 'Pendente'),
        ('Aprovado', 'Aprovado'),
        ('Negado', 'Negado')
    ])

