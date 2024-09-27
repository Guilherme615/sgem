from django.urls import path
from .views import (
    login_view, home, register_view, cadastrar_produto, lista_produtos, movimentar_estoque, 
    lista_movimentos, cadastrar_fornecedor, lista_fornecedores, relatorio_entrada_saida, 
    relatorio_validade_produtos, historico_movimentacoes, lista_usuarios, cadastrar_usuario,
    inventario_view, logout_view, editar_produto,
    excluir_produto  # Importando a nova view
)

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('produtos/', lista_produtos, name='lista_produtos'),
    path('produtos/cadastrar/', cadastrar_produto, name='cadastrar_produto'),
    path('produtos/editar/<int:id>/', editar_produto, name='editar_produto'),
    path('produtos/excluir/<int:id>/', excluir_produto, name='excluir_produto'),
    path('estoque/movimentar/', movimentar_estoque, name='movimentar_estoque'),
    path('estoque/movimentos/', lista_movimentos, name='lista_movimentos'),
    path('fornecedores/', lista_fornecedores, name='lista_fornecedores'),
    path('fornecedores/cadastrar/', cadastrar_fornecedor, name='cadastrar_fornecedor'),
    path('relatorios/entrada-saida/', relatorio_entrada_saida, name='relatorio_entrada_saida'),
    path('relatorios/validade/', relatorio_validade_produtos, name='relatorio_validade_produtos'),
    path('historico/movimentacoes/', historico_movimentacoes, name='historico_movimentacoes'),
    path('usuarios/', lista_usuarios, name='lista_usuarios'),
    path('usuarios/cadastrar/', cadastrar_usuario, name='cadastrar_usuario'),
    path('inventario/', inventario_view, name='inventario'),  # Adicionando a URL para o inventário
]
