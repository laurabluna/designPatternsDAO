

from typing import Any
from .dominio import *
from abc import ABC, abstractmethod
import sqlite3


class DAO(ABC):

    _conexao: sqlite3.Connection

    @abstractmethod
    def incluir(self, obj: Any): pass

    @abstractmethod
    def alterar(self, obj: Any): pass

    @abstractmethod
    def excluir(self, obj: Any): pass

    @abstractmethod
    def selecionar_todos(self) -> list[Any]: pass

    @abstractmethod
    def selecionar_um(id: int) -> Any: pass

    def obter_conexao(self):
        self._conexao = sqlite3.connect('arq_soft.sqlite3')
        return self._conexao

    def fechar_conexao(self):
        if self._conexao is not None:
            self._conexao.close()

    def executar_sql(self, sql, commit=True) -> Any:
        '''Executa um comando SQL no BD (geralmente um INSERT, UPDATE ou DELETE)'''
        # obtem conexao
        conexao = self.obter_conexao()
        # cria um cursor() e executa o SQL informado
        ret = conexao.cursor().execute(sql)
        # verifica se eh para efetivar as modificações no BD
        if commit:
            conexao.commit()
        # retorna o resultado do metodo execute()
        return ret 

    def executar_select(self, sql) -> list[Any]:
        '''Executa um comando SELECT no BD e retorna os registros'''
        # obtem conexao
        conexao = self.obter_conexao()
        # cria um cursor(), executa o SELECT informado e traz os todos os registros
        ret = conexao.cursor().execute(sql).fetchall()
        # retorna os registros do BD
        return ret 
    

class CategoriaDAO(DAO):
    
    def incluir(self, obj:Categoria):
        sql = f"INSERT INTO Categoria(descricao) VALUES('{obj.descricao}')"
        self.executar_sql(sql)

    def alterar(self, obj:Categoria):
        sql = f'''  UPDATE Categoria 
                    SET descricao = '{obj.descricao}' 
                    WHERE id = {obj.id}'''        
        self.executar_sql(sql)

    def excluir(self, obj:Categoria):
        sql = f"DELETE FROM Categoria WHERE id = {obj.id}"
        self.executar_sql(sql)

    def selecionar_todos(self) -> list[Categoria]: 
        # seleciona as categorias
        sql = '''   SELECT  id, descricao FROM Categoria ORDER BY descricao '''
        # obtem todos os registros retornados
        registros = self.executar_select(sql)
        # converte os registros para objetos e adiciona na lista
        dados = list()
        for reg in registros:
            dados.append( Categoria(id=reg[0], descricao=reg[1]) )
        # retorna
        return dados

    def selecionar_um(self, id: int) -> Categoria: 
        # seleciona o registro pelo id informado
        sql = f'''  SELECT  id, descricao FROM Categoria WHERE id={id} '''
        # executa o select e pega o primeiro registro([0])
        reg = self.executar_select(sql)[0]
        # converte o registro para objeto e retorna
        return Categoria(id=reg[0], descricao=reg[1])
    
class ProdutoDAO(DAO):
    
    def incluir(self, obj:Produto):
        sql = f'''  INSERT INTO Produto(descricao, preco_unitario, categoria_id) 
                    VALUES('{obj.descricao}', {obj.preco_unitario}, {obj.categoria.id}) '''
        self.executar_sql(sql)

    def alterar(self, obj:Produto):
        sql = f'''  UPDATE Produto 
                    SET descricao = '{obj.descricao}', 
                        preco_unitario = {obj.preco_unitario}, 
                        categoria_id = {obj.categoria.id} 
                    WHERE id = {obj.id} '''        
        self.executar_sql(sql)

    def excluir(self, obj:Produto):
        sql = f"DELETE FROM Produto WHERE id = {obj.id}"
        self.executar_sql(sql)

    def selecionar_todos(self) -> list[Produto]: 
        # seleciona os produtos
        sql = '''   SELECT  p.id, p.descricao, p.preco_unitario, c.id, c.descricao 
                    FROM Produto p JOIN Categoria c ON p.categoria_id=c.id 
                    ORDER BY p.descricao '''
       
        registros = self.executar_select(sql)
      
        dados = list()
        for reg in registros:
            dados.append( Produto(id=reg[0], descricao=reg[1], preco_unitario=reg[2], categoria=Categoria(id=reg[3], descricao=reg[4])) )
      
        return dados

    def selecionar_um(self, id: int) -> Produto: 
       
        sql = f'''  SELECT  p.id, p.descricao, p.preco_unitario, c.id, c.descricao 
                    FROM Produto p JOIN Categoria c ON p.categoria_id=c.id 
                    WHERE p.id={id} '''
    
        reg = self.executar_select(sql)[0]
        return Produto(id=reg[0], descricao=reg[1], preco_unitario=reg[2], categoria=Categoria(id=reg[3], descricao=reg[4]))
