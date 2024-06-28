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
        #TODO: COLOCAR SEM CATEGORIA NO ESTOQUE
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
                #TODO: ALTERAR A CATEGORIA TAMBEM DO ESTOQUE
            else:
                print("A categoria para qual deseja alterar já existente")

        else:
            print("A categoria que deseja alterar não existe")

        with open('categoria.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.categoria)
                arq.writelines('\n')

    def mostra_Categoria(self):
        categoria = DaoCategoria.ler()
        if len(categoria) == 0:
            print('Categoria Vazia')
        else:
            for i in categoria:
                print(f'Categoria {i.categoria}')

class ControllerEstoque:
    def cadastraProduto(self, nome, preco, categoria, quantidade):
        x = DaoEstoque.ler()
        y = DaoCategoria.ler()
        h = list(filter(lambda x: x.categoria == categoria, y))
        est = list(filter(lambda x: x.produto.nome == nome, x))

        if len(h) > 0:
            if len(est) == 0:
                produto = Produtos(nome, preco, categoria)
                DaoEstoque.salvar(produto, quantidade)
                print('Produto cadastrada com sucesso')
            else:
                print('Produto já exite em estoque')
        else:
            print('Categoria não existe')

    def removerProduto(self, nome):
        x = DaoEstoque.ler()
        est = list(filter(lambda x: x.produto.nome == nome, x))
        if len(est) > 0:
            for i in range(len(x)):
               if x[i].produto.nome == nome:
                   del x[i]
                   break
            print('Produto removido com sucesso')
        else:
            print('O produto que deseja remover não existe')

        with open('estoque.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.produto.nome + "|" + i.produto.preco + "|" +
                           i.produto.categoria + "|" + str(i.quantidade))
                arq.writelines('\n')

    def alterarProduto(self, nomeAlterar, novoNome, novoPreco, novaCategoria, novaQuantidade):
        x = DaoEstoque.ler()
        y = DaoCategoria.ler()
        h = list(filter(lambda x: x.categoria == novaCategoria, y))
        if len(h) > 0:
              est = list(filter(lambda x: x.produto.nome == nomeAlterar, x))
              if len(est) > 0:
                  est = list(filter(lambda x: x.produto.nome == novoNome, x))
                  if len(est) == 0:
                      x = list(map(lambda x: Estoque(Produtos(novoNome, novoPreco, novaCategoria), novaQuantidade) if (x.produto.nome == nomeAlterar) else(x), x))
                      print("Estoque alterada com sucesso")
                  else:
                      print('Produto já cadastrado')
              else:
                  print('O produto que deseja alterar não existe')

              with open('estoque.txt', 'w') as arq:
                  for i in x:
                      arq.writelines(i.produto.nome + "|" + i.produto.preco + "|" +
                                     i.produto.categoria + "|" + str(i.quantidade))
                      arq.writelines('\n')
        else:
              print('A categoria informada não existe')

    def mostraEstoque(self):
        estoque = DaoEstoque.ler()
        if len(estoque) == 0:
            print('Estoque vazio')
        else:

            for i in estoque:
                print('==========Produto==========')
                print(f'Categoria: {i.produto.categoria}')
                print(f'Nome: {i.produto.nome}')
                print(f'Preço: {i.produto.preco}')
                print(f'Quantidade: {i.quantidade}')
            print('-------------------------------')

class ControllerVenda:
    def cadastrarVenda(self, nomeProduto, vendedor, comprador, quantidadeVendida):

        x = DaoEstoque.ler()
        temp = []
        existe = False
        quantidade = False

        for i in x:
            if existe == False:
                if i.produto.nome == nomeProduto:
                    existe = True
                    if i.quantidade >= quantidadeVendida:
                        quantidade = True
                        i.quantidade = int(i.quantidade) - int(quantidadeVendida)

                        vendido = Venda(Produtos(i.produto.nome, i.produto.preco, i.produto.categoria), vendedor, comprador, quantidadeVendida )

                        valorCompra = int(quantidadeVendida) * int(i.produto.preco)

                        DaoVenda.salvar(vendido)
            temp.append([Produtos(i.produto.nome, i.produto.preco, i.produto.categoria), i.quantidade])

            arq = open('estoque.txt', 'w')
            arq.write("")

            for i in temp:
                with open ('estoque.txt', 'a') as arq:
                    arq.writelines(i[0].nome + "|" + i[0].preco + "|" + i[0].categoria + "|" + str(i[1]))
                    arq.writelines('\n')

            if existe == False:
                print('O produto não existe')
                return None
            elif not quantidade:
                print('A quantidade vendida não contem em estoque')
                return None
            else:
                print('Venda realizada com sucesso')
                return  valorCompra

    def relatorioVendas(self):
        vendas = DaoVenda.ler()
        produtos = []
        for i in vendas:
            nome = i.itensVendidos.nome
            quantidade = i.quantidadeVendidas
            tamanho = list(filter(lambda x: x['produto'] == nome, produtos))
            if len(tamanho) > 0:
                produtos = list(map(lambda x: {'produto': nome, 'quantidade': x['quantidade'] + quantidade}
                                    if (x['produto'] == nome) else (x), produtos))
            else:
                produtos.append({'produto': nome, 'quantidade': quantidade})

            ordenado = sorted(produtos, key=lambda k: k['quantidade'], reverse=True)

            print("Esses são os produtos vendidos")
            a = 1
            for i in ordenado:
                print(f"==========PRODUTOS [{a}=============")
                print(f"produto: {i['produto']}\n"
                      f"quantidade: {i['quantidade']}\n")
                a += 1

a = ControllerEstoque()
a.cadastraProduto("manga", "10","Frutas", "100")
