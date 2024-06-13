from models import Categoria, Estoque, Produtos, Fornecedor, Pessoa, Funcionario, Venda
from DAO import DaoCategoria, DaoVenda, DaoFuncionario, DaoEstoque, DaoPessoas, DaoFornecedor
from datetime import datetime

class ControllerCategoria:
    def cadastra_Categoria(self, novaCategoria):
        existe = False
        x = DaoCategoria.ler()
        for i in x:
            if i.categoria == novaCategoria:
                existe = True

        if not existe:
            DaoCategoria.salvar(novaCategoria)
            print('Categoria cadastrada com sucesso')

        else:
            print('Categoria já existente')


    def remover_Categoria(self, categoriaRemover):
        x = DaoCategoria.ler()
        cat = list(filter(lambda x: x.categoria == categoriaRemover, x))

        if len(cat) <= 0:
            print('A categoria que deseja remover não existe')

        else:
            for i in range(len(x)):
                if x[i].categoria == categoriaRemover:
                    del x[i]
                    break
            print('Categoria removida com sucesso')

            with open('categoria.txt',  'w') as arq:
                for i in x:
                    arq.writelines(i.categoria)
                    arq.writelines('\n')


    def alterarCAtegoria(self, categoriaAlterar, categoriaAterada):
        x = DaoCategoria.ler()

        cat = list(filter(lambda x: x.categoria == categoriaAlterar, x))

        if len(cat) > 0:
            cat1 = list(filter(lambda x: x.categoria == categoriaAterada, x))
            if len(cat1) == 0:
                x = list(map(lambda x: Categoria(categoriaAterada)if(x.categoria == categoriaAlterar) else(x), x))
                print("Categoria alterada com sucesso")
            else:
                print("A categoria para qual deseja alterar já existente")

        else:
            print("A categoria que deseja alterar não existe")

        with open('categoria.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.categoria)
                arq.writelines('\n')


a = ControllerCategoria()
a.alterarCAtegoria("CArnes", "Verduras")