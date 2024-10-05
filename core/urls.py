from django.urls import path
from . import views
from .views import (
    login_view, home, register_view, cadastrar_produto, lista_produtos, 
    lista_movimentos, relatorio_entrada_saida, 
    relatorio_validade_produtos, historico_movimentacoes, lista_usuarios, cadastrar_usuario, logout_view, editar_produto,
    excluir_produto
)
from django.contrib import messages  # Importar mensagens

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('produtos/', lista_produtos, name='lista_produtos'),
    path('produtos/cadastrar/', cadastrar_produto, name='cadastrar_produto'),
    path('produtos/editar/<int:id>/', editar_produto, name='editar_produto'),
    path('produtos/excluir/<int:id>/', excluir_produto, name='excluir_produto'),
    path('lista-movimentos/', lista_movimentos, name='lista_movimentos'),
    path('relatorio-entrada-saida/', relatorio_entrada_saida, name='relatorio_entrada_saida'),
    path('relatorios/validade/', relatorio_validade_produtos, name='relatorio_validade_produtos'),
    path('historico/movimentacoes/', historico_movimentacoes, name='historico_movimentacoes'),
    path('usuarios/', lista_usuarios, name='lista_usuarios'),
    path('usuarios/cadastrar/', cadastrar_usuario, name='cadastrar_usuario'),
    path('produtos/excluir/<int:id>/', views.excluir_produto, name='excluir_produto'),
    path('produtos/lixeira/', views.lixeira_produtos, name='lixeira_produtos'),
    path('produtos-proximos-validade/', views.produtos_proximos_validade, name='produtos_proximos_validade'),

]