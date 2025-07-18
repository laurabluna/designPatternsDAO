from django.http import HttpResponseRedirect
from django.shortcuts import render
import sys

from django.urls import reverse
from utils import helper

from .dominio import *
from .dao import *


def home(request):
    '''Exibe a pagina inicial da aplicação'''
    # define a página HTML (template) que deverá será carregada
    template = 'home.html'
    return render(request, template)


def categorias(request, acao=None, id=None):
    try:
        # DAO que utilizado neste metodo
        dao = CategoriaDAO()

        # listar registros 
        if acao is None:
            # define o comando SQL que será executado
            registros = dao.selecionar_todos()
            # define a pagina a ser carregada, adicionando os registros das tabelas 
            return render(request, 'categorias_listar.html', context={'registros': registros})
        
        # salvar registro
        elif acao == 'salvar':
            form_data = request.POST
            acao_form = form_data['acao']

            if acao_form == 'Inclusão':
                obj = Categoria(id=None, descricao=form_data['descricao'])
                dao.incluir(obj)

            elif acao_form == 'Exclusão':
                obj = Categoria(id=form_data['id'], descricao=None)
                dao.excluir(obj)

            else:
                obj = Categoria(id=form_data['id'], descricao=form_data['descricao'])
                dao.alterar(obj)

            # Sempre retornar um HttpResponseRedirect após processar dados "POST". 
            # Isso evita que os dados sejam postados 2 vezes caso usuário clicar "Voltar".
            return HttpResponseRedirect( reverse("categorias") )
        
        # inserir registro
        elif acao == 'incluir':
            return render(request, 'categorias_editar.html', {'acao': 'Inclusão'})
        
        # alterar ou excluir
        elif acao in ['alterar', 'excluir']:
            acao = 'Alteração' if acao == 'alterar' else 'Exclusão'
            # seleciona o registro pelo id informado
            obj = dao.selecionar_um(id)
            return render(request, 'categorias_editar.html', {'acao': acao, 'obj': obj})
        
        # acao INVALIDA
        else:
            raise Exception('Ação inválida')

    # se ocorreu algunm erro, insere a mensagem para ser exibida no contexto da página 
    except Exception as err:
        return render(request, 'home.html', context={'ERRO': err})


def produtos(request, acao=None, id=None):
    try:
        dao = ProdutoDAO()
        cat_dao = CategoriaDAO()

        if acao is None:
            registros = dao.selecionar_todos()
            return render(request, 'produtos_listar.html', context={'registros': registros})

        elif acao == 'salvar':
            form_data = request.POST
            acao_form = form_data['acao']

            if acao_form == 'Inclusão':
                categoria = cat_dao.selecionar_um(int(form_data['categoria_id']))
                obj = Produto(
                    id=None,
                    descricao=form_data['descricao'],
                    preco_unitario=form_data['preco_unitario'],
                    quantidade_estoque=form_data['quantidade_estoque'] or None,
                    categoria=categoria
                )
                dao.incluir(obj)

            elif acao_form == 'Exclusão':
                obj = Produto(
                    id=form_data['id'],
                    descricao=None,
                    preco_unitario=None,
                    quantidade_estoque=None,
                    categoria=Categoria(id=0, descricao='')
                )
                dao.excluir(obj)

            else:
                categoria = cat_dao.selecionar_um(int(form_data['categoria_id']))
                obj = Produto(
                    id=form_data['id'],
                    descricao=form_data['descricao'],
                    preco_unitario=form_data['preco_unitario'],
                    quantidade_estoque=form_data['quantidade_estoque'] or None,
                    categoria=categoria
                )
                dao.alterar(obj)

            return HttpResponseRedirect(reverse("produtos"))

        elif acao == 'incluir':
            categorias = cat_dao.selecionar_todos()
            return render(request, 'produtos_editar.html', {'acao': 'Inclusão', 'categorias': [(c.id, c.descricao) for c in categorias]})

        elif acao in ['alterar', 'excluir']:
            obj = dao.selecionar_um(id)
            categorias = cat_dao.selecionar_todos()
            acao_nome = 'Alteração' if acao == 'alterar' else 'Exclusão'
            return render(request, 'produtos_editar.html', {
                'acao': acao_nome,
                'obj': obj,
                'categorias': [(c.id, c.descricao) for c in categorias]
            })

        else:
            raise Exception('Ação inválida')

    except Exception as err:
        return render(request, 'home.html', context={'ERRO': err})



