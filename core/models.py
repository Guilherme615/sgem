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
    is_deleted = models.BooleanField(default=False)  # Campo para marcar produtos excluídos

    def __str__(self):
        return self.nome

# Modelo para Registro de Entrada e Saída de Produtos no Estoque
class MovimentoEstoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=[('adicao', 'Adição'), ('edicao', 'Edição'), ('exclusao', 'Exclusão')])
    quantidade = models.IntegerField()
    data_movimento = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Permitir nulos

    def __str__(self):
        return f'{self.tipo} - {self.produto.nome} ({self.quantidade})'
