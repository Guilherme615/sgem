from django.db import models
from django.contrib.auth.models import User

# Modelo para Categorias de Produtos (Ex: Alimentos, Bebidas)
class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

# Modelo para Produtos
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    data_validade = models.DateField()

    def __str__(self):
        return self.nome

class Fornecedor(models.Model):
    nome = models.CharField(max_length=255)
    contato = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()
    pontualidade = models.IntegerField(help_text="Avaliação de 0 a 5")

    def __str__(self):
        return self.nome

# Modelo para Registro de Entrada e Saída de Produtos no Estoque
class MovimentoEstoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=[('adicao', 'Adição'), ('edicao', 'Edição'), ('exclusao', 'Exclusão')])
    quantidade = models.IntegerField()
    data_movimento = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Permitir nulos
