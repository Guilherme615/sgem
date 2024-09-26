from django.urls import path
from .views import (
    login_view, home, register_view, cadastrar_produto, lista_produtos, movimentar_estoque, 
    lista_movimentos, cadastrar_fornecedor, lista_fornecedores, relatorio_entrada_saida, 
    relatorio_validade_produtos, historico_movimentacoes, lista_usuarios, cadastrar_usuario
)

urlpatterns = [
    path('', home, name='home'),  # URL para a página inicial
    path('login/', login_view, name='login'),  # URL para a tela de login
    path('register/', register_view, name='register'),  # URL para a página de cadastro
    path('produtos/', lista_produtos, name='lista_produtos'),  # Listagem de produtos
    path('produtos/cadastrar/', cadastrar_produto, name='cadastrar_produto'),  # Cadastro de produtos
    path('estoque/movimentar/', movimentar_estoque, name='movimentar_estoque'),  # Movimentação de estoque
    path('estoque/movimentos/', lista_movimentos, name='lista_movimentos'),  # Listagem de movimentos de estoque
    path('fornecedores/', lista_fornecedores, name='lista_fornecedores'),  # Listagem de fornecedores
    path('fornecedores/cadastrar/', cadastrar_fornecedor, name='cadastrar_fornecedor'),  # Cadastro de fornecedores
]

# Adicionando as URLs para relatórios, histórico de movimentações e gestão de usuários
urlpatterns += [
    path('relatorios/entrada-saida/', relatorio_entrada_saida, name='relatorio_entrada_saida'),  # Relatório de entrada e saída
    path('relatorios/validade/', relatorio_validade_produtos, name='relatorio_validade_produtos'),  # Relatório de validade de produtos
    path('historico/movimentacoes/', historico_movimentacoes, name='historico_movimentacoes'),  # Histórico de movimentações
    path('usuarios/', lista_usuarios, name='lista_usuarios'),  # Listagem de usuários
    path('usuarios/cadastrar/', cadastrar_usuario, name='cadastrar_usuario'),  # Cadastro de usuários
]
