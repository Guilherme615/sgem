import os
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from .models import Produto, MovimentoEstoque, Categoria
from .forms import LoginForm, RegistrationForm, MovimentoEstoqueForm, UsuarioForm
from django.contrib import messages

# Página inicial
def home(request):
    return render(request, 'index.html')

# View de login
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redireciona para a página inicial após o login
            else:
                form.add_error(None, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

# View de registro
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Definindo a senha
            user.save()
            login(request, user)  # Faz login automático do usuário após o registro
            messages.success(request, 'Conta criada com sucesso!')  # Mensagem de sucesso
            return redirect('home')  # Redireciona para a página inicial
        else:
            messages.error(request, 'Erro ao criar conta. Verifique os dados.')  # Mensagem de erro
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

# Logout do usuário
def logout_view(request):
    logout(request)
    return redirect('login')

# View para cadastrar produto
def cadastrar_produto(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        categoria_nome = request.POST.get('categoria')
        quantidade = request.POST.get('quantidade')
        data_validade = request.POST.get('data_validade')

        if not nome or not categoria_nome or not quantidade or not data_validade:
            messages.error(request, 'Todos os campos devem ser preenchidos.')
            return redirect('cadastrar_produto')

        categoria, created = Categoria.objects.get_or_create(nome=categoria_nome)

        produto = Produto(
            nome=nome,
            categoria=categoria,
            quantidade=quantidade,
            data_validade=data_validade
        )
        produto.save()

        # Registra como "entrada" no movimento de estoque
        movimento = MovimentoEstoque(
            produto=produto,
            tipo='entrada',
            quantidade=quantidade,
            usuario=request.user
        )
        movimento.save()

        return redirect('lista_produtos')

    categorias = Categoria.objects.all()
    return render(request, 'cadastrar_produto.html', {'categorias': categorias})


# View para listar produtos
def lista_produtos(request):
    produtos = Produto.objects.filter(is_deleted=False)  # Filtra produtos que não estão na lixeira
    return render(request, 'lista_produtos.html', {'produtos': produtos})


# View para editar produto
def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)

    if request.method == 'POST':
        produto.nome = request.POST.get('nome')
        categoria_nome = request.POST.get('categoria')
        categoria, created = Categoria.objects.get_or_create(nome=categoria_nome)
        produto.categoria = categoria
        produto.quantidade = request.POST.get('quantidade')
        produto.data_validade = request.POST.get('data_validade')
        produto.save()

        # Registra a edição no movimento de estoque
        movimento = MovimentoEstoque(
            produto=produto,
            tipo='edicao',
            quantidade=produto.quantidade,  # Pode ser a quantidade atual ou a que foi editada
            usuario=request.user
        )
        movimento.save()

        return redirect('lista_produtos')

    categorias = Categoria.objects.all()
    return render(request, 'editar_produto.html', {'produto': produto, 'categorias': categorias})

# View para excluir produto
def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    
    produto.is_deleted = True
    produto.save()

    # Registra como "saída" no movimento de estoque
    movimento = MovimentoEstoque(
        produto=produto,
        tipo='saida',
        quantidade=produto.quantidade,
        usuario=request.user
    )
    movimento.save()

    return redirect('lista_produtos')


# View para movimentação de estoque
def movimentar_estoque(request):
    if request.method == 'POST':
        form = MovimentoEstoqueForm(request.POST)
        if form.is_valid():
            movimento = form.save(commit=False)
            movimento.data_movimento = timezone.now()  # Set the date manually here
            movimento.usuario = request.user  # Associate the movement with the logged-in user
            movimento.save()
            return redirect('lista_movimentos')
    else:
        form = MovimentoEstoqueForm()
    return render(request, 'movimentar_estoque.html', {'form': form})

# View para listar movimentações de estoque
def lista_movimentos(request):
    movimentos = MovimentoEstoque.objects.all()
    print(f"Total de movimentos: {movimentos.count()}")  # Para debug
    return render(request, 'lista_movimentos.html', {'movimentos': movimentos})
# Função auxiliar para gerar PDF
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erro ao gerar o PDF', status=400)
    return response

# Relatório de Entrada e Saída de Produtos
def relatorio_entrada_saida(request):
    # Filtra apenas entradas e saídas (removendo edições do relatório)
    movimentos = MovimentoEstoque.objects.filter(tipo__in=['entrada', 'saida']).order_by('-data_movimento')

    if request.method == 'POST' and 'limpar_relatorio' in request.POST:
        MovimentoEstoque.objects.all().delete()
        return redirect('relatorio_entrada_saida')

    if request.GET.get('format') == 'pdf':
        context = {'movimentos': movimentos}
        pdf = render_to_pdf('relatorio_entrada_saida_pdf.html', context)
        return pdf

    return render(request, 'relatorio_entrada_saida.html', {'movimentos': movimentos})

# Relatório de Validade de Produtos
def relatorio_validade_produtos(request):
    produtos = Produto.objects.filter(data_validade__lt=timezone.now())
    return render(request, 'relatorio_validade_produtos.html', {'produtos': produtos})

# Histórico de Movimentações
def historico_movimentacoes(request):
    movimentos = MovimentoEstoque.objects.all()
    return render(request, 'historico_movimentacoes.html', {'movimentos': movimentos})

# Cadastrar Usuários
def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'cadastrar_usuario.html', {'form': form})

# Lista de Usuários
def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})

def lixeira_produtos(request):
    produtos_excluidos = Produto.objects.filter(is_deleted=True)  # Lista os produtos na lixeira
    return render(request, 'lixeira_produtos.html', {'produtos_excluidos': produtos_excluidos})

def produtos_proximos_validade(request):
    hoje = timezone.now().date()
    uma_semana_antes = hoje + timedelta(weeks=1)
    
    # Filtra produtos cuja validade é dentro de 1 semana e ainda não expirou
    produtos_perto_validade = Produto.objects.filter(data_validade__range=[hoje, uma_semana_antes])

    return render(request, 'produtos_proximos_validade.html', {
        'produtos_perto_validade': produtos_perto_validade
    })

def navbar_info(request):
    hoje = timezone.now().date()
    uma_semana_antes = hoje + timedelta(weeks=1)

    # Verifica se existem produtos próximos da validade
    produtos_perto_validade = Produto.objects.filter(data_validade__range=[hoje, uma_semana_antes]).exists()

    return {
        'produtos_proximos_validade': produtos_perto_validade,
    }