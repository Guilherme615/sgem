import os
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Produto, MovimentoEstoque, Fornecedor, Categoria
from .forms import LoginForm, RegistrationForm, MovimentoEstoqueForm, FornecedorForm, UsuarioForm
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
        categoria_nome = request.POST.get('categoria')  # O usuário vai digitar o nome da categoria
        quantidade = request.POST.get('quantidade')
        data_validade = request.POST.get('data_validade')

        # Verifique se a categoria existe, se não, crie uma nova
        categoria, created = Categoria.objects.get_or_create(nome=categoria_nome)

        # Criar e salvar o produto
        produto = Produto(
            nome=nome,
            categoria=categoria,
            quantidade=quantidade,
            data_validade=data_validade
        )
        produto.save()

        return redirect('lista_produtos')  # Redireciona após salvar

    # Obtém todas as categorias para dropdown no formulário
    categorias = Categoria.objects.all()  
    return render(request, 'cadastrar_produto.html', {'categorias': categorias})

# View para listar produtos
def lista_produtos(request):
    produtos = Produto.objects.all()  # Obtenha todos os produtos
    return render(request, 'lista_produtos.html', {'produtos': produtos})

# View para editar produto
def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)

    if request.method == 'POST':
        produto.nome = request.POST.get('nome')
        
        # Obtém o nome da categoria fornecido no formulário
        categoria_nome = request.POST.get('categoria')
        
        # Busca ou cria a categoria com o nome fornecido
        categoria, created = Categoria.objects.get_or_create(nome=categoria_nome)
        
        produto.categoria = categoria  # Associa a categoria ao produto
        produto.quantidade = request.POST.get('quantidade')
        produto.data_validade = request.POST.get('data_validade')
        produto.save()

        return redirect('lista_produtos')

    categorias = Categoria.objects.all()  # Para o dropdown de categorias
    return render(request, 'editar_produto.html', {'produto': produto, 'categorias': categorias})

# View para excluir produto
def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    return redirect('lista_produtos')

# View para movimentação de estoque
def movimentar_estoque(request):
    if request.method == 'POST':
        form = MovimentoEstoqueForm(request.POST)
        if form.is_valid():
            movimento = form.save(commit=False)
            movimento.usuario = request.user  # Associe o movimento ao usuário logado
            movimento.save()
            return redirect('lista_movimentos')
    else:
        form = MovimentoEstoqueForm()
    return render(request, 'movimentar_estoque.html', {'form': form})

# View para listar movimentações de estoque
def lista_movimentos(request):
    movimentos = MovimentoEstoque.objects.all()
    return render(request, 'lista_movimentos.html', {'movimentos': movimentos})

# Cadastro de Fornecedores
def cadastrar_fornecedor(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_fornecedores')
    else:
        form = FornecedorForm()
    return render(request, 'cadastrar_fornecedor.html', {'form': form})

# Consulta de Fornecedores
def lista_fornecedores(request):
    fornecedores = Fornecedor.objects.all()
    return render(request, 'lista_fornecedores.html', {'fornecedores': fornecedores})

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
    movimentos = MovimentoEstoque.objects.all()
    
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
