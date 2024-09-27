from django.db import models

# Modelo para Categorias de Produtos (Ex: Alimentos, Bebidas)
class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

# Modelo para Produtos
class Produto(models.Model):
    nome = models.CharField(max_length=255)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    data_validade = models.DateField()

    def __str__(self):
        return self.nome


# Modelo para Registro de Entrada e Saída de Produtos no Estoque
class MovimentoEstoque(models.Model):
    TIPO_MOVIMENTO = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=7, choices=TIPO_MOVIMENTO)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    data_movimento = models.DateField()
    fornecedor = models.CharField(max_length=200, blank=True, null=True)
    nota_fiscal = models.CharField(max_length=100, blank=True, null=True)
    destino = models.CharField(max_length=200, blank=True, null=True)  # Usado para saída

    def __str__(self):
        return f'{self.tipo.capitalize()} - {self.produto.nome}'

class Fornecedor(models.Model):
    nome = models.CharField(max_length=255)
    contato = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()
    pontualidade = models.IntegerField(help_text="Avaliação de 0 a 5")

    def __str__(self):
        return self.nome
