from django.urls import path
from . import views
from .views import (
    login_view, home, register_view, cadastrar_produto, lista_produtos, 
    relatorio_entrada_saida, 
    historico_movimentacoes, 
    logout_view, editar_produto, excluir_produto, 
    pedidos_view, admin_dashboard, lixeira_produtos, produtos_proximos_validade, 
    lista_pedidos, gerenciar_pedidos, aprovar_pedido, negar_pedido, excluir_pedido,
    criar_escola
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
    path('relatorio-entrada-saida/', relatorio_entrada_saida, name='relatorio_entrada_saida'),
    path('historico/movimentacoes/', historico_movimentacoes, name='historico_movimentacoes'),
    path('produtos/lixeira/', lixeira_produtos, name='lixeira_produtos'),
    path('produtos-proximos-validade/', produtos_proximos_validade, name='produtos_proximos_validade'),
    path('dashboard-admin/', admin_dashboard, name='admin_dashboard'),
    path('pedidos/', pedidos_view, name='pedidos'),  # Página de fazer pedidos
    path('pedidos/lista/', lista_pedidos, name='lista_pedidos'),  # Lista de pedidos
    path('excluir-pedido/<int:pedido_id>/', excluir_pedido, name='excluir_pedido'),
    path('gerenciar-pedidos/', gerenciar_pedidos, name='gerenciar_pedidos'),
    path('aprovar-pedido/<int:pedido_id>/', aprovar_pedido, name='aprovar_pedido'),
    path('negar-pedido/<int:pedido_id>/', negar_pedido, name='negar_pedido'),
    path('criar-escola/', criar_escola, name='criar_escola'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('excluir_usuario/<int:user_id>/', views.excluir_usuario, name='excluir_usuario'),
]
