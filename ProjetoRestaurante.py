from datetime import datetime


class No:
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None


class ListaEncadeada:
    def __init__(self):
        self.inicio = None

    def adicionar(self, dado):
        novo_no = No(dado)
        if self.inicio is None:
            self.inicio = novo_no
        else:
            atual = self.inicio
            while atual.proximo:
                atual = atual.proximo
            atual.proximo = novo_no

    def remover(self, dado):
        if self.inicio is None:
            return False
        if self.inicio.dado == dado:
            self.inicio = self.inicio.proximo
            return True
        atual = self.inicio
        while atual.proximo:
            if atual.proximo.dado == dado:
                atual.proximo = atual.proximo.proximo
                return True
            atual = atual.proximo
        return False

    def listar(self):
        itens = []
        atual = self.inicio
        while atual:
            itens.append(atual.dado)
            atual = atual.proximo
        return itens


class Item:
    def __init__(self, nome, preco, tipo):
        self.nome = nome
        self.preco = preco
        self.tipo = tipo

    def __eq__(self, other):
        return isinstance(other, Item) and self.nome == other.nome and self.tipo == other.tipo


class Comanda:
    def __init__(self, numero, cliente):
        self.numero = numero
        self.cliente = cliente
        self.data_hora = datetime.now()
        self.refeicoes = ListaEncadeada()
        self.bebidas = ListaEncadeada()
        self.fechada = False

    def adicionar_item(self, item):
        if not self.fechada:
            if item.tipo == 'refeicao':
                self.refeicoes.adicionar(item)
            elif item.tipo == 'bebida':
                self.bebidas.adicionar(item)

    def remover_item(self, item):
        if not self.fechada:
            if item.tipo == 'refeicao':
                return self.refeicoes.remover(item)
            elif item.tipo == 'bebida':
                return self.bebidas.remover(item)
        return False

    def fechar(self):
        self.fechada = True

    def total(self):
        soma = 0
        for item in self.refeicoes.listar() + self.bebidas.listar():
            soma += item.preco
        return soma


class GerenciadorComandas:
    def __init__(self):
        self.comandas = ListaEncadeada()
        self.prox_numero = 1

    def abrir(self, cliente):
        comanda = Comanda(self.prox_numero, cliente)
        self.comandas.adicionar(comanda)
        self.prox_numero += 1
        return comanda

    def buscar(self, numero):
        for c in self.comandas.listar():
            if c.numero == numero:
                return c
        return None

    def fechar(self, numero):
        comanda = self.buscar(numero)
        if comanda and not comanda.fechada:
            comanda.fechar()
            return True
        return False

    def abertas(self):
        return [c for c in self.comandas.listar() if not c.fechada]


# === PARTE 2: CONTROLE DE ESTOQUE ===

class FilaEncadeada:
    def __init__(self):
        self.inicio = None
        self.fim = None

    def enfileirar(self, dado):
        novo_no = No(dado)
        if self.inicio is None:
            self.inicio = novo_no
            self.fim = novo_no
        else:
            self.fim.proximo = novo_no
            self.fim = novo_no

    def desenfileirar(self):
        if self.inicio is None:
            return None
        dado = self.inicio.dado
        self.inicio = self.inicio.proximo
        if self.inicio is None:
            self.fim = None
        return dado

    def listar(self):
        itens = []
        atual = self.inicio
        while atual:
            itens.append(atual.dado)
            atual = atual.proximo
        return itens


class Produto:
    def __init__(self, nome, preco_compra, preco_venda, data_compra, data_vencimento, quantidade):
        self.nome = nome
        self.preco_compra = preco_compra
        self.preco_venda = preco_venda
        self.data_compra = data_compra
        self.data_vencimento = data_vencimento
        self.quantidade = quantidade

    def editar_quantidade(self, nova_qtd):
        self.quantidade = nova_qtd


class GerenciadorEstoque:
    def __init__(self):
        self.produtos = FilaEncadeada()

    def adicionar_produto(self, produto):
        self.produtos.enfileirar(produto)

    def remover_produto_antigo(self):
        return self.produtos.desenfileirar()

    def buscar_produto(self, nome):
        for p in self.produtos.listar():
            if p.nome == nome:
                return p
        return None

    def editar_quantidade(self, nome, nova_qtd):
        produto = self.buscar_produto(nome)
        if produto:
            produto.editar_quantidade(nova_qtd)
            return True
        return False

    def listar_estoque(self):
        return self.produtos.listar()


# === PARTE 3: CONTROLE DE PAGAMENTO ===

class Pagamento:
    def __init__(self, cliente, numero_comanda, forma_pagamento, valor, data_hora):
        self.cliente = cliente
        self.numero_comanda = numero_comanda
        self.forma_pagamento = forma_pagamento  # PIX, cartao, dinheiro
        self.valor = valor
        self.data_hora = data_hora


class GerenciadorPagamentos:
    def __init__(self):
        self.pagamentos = ListaEncadeada()

    def registrar_pagamento(self, pagamento):
        self.pagamentos.adicionar(pagamento)

    def buscar_pagamentos_por_comanda(self, numero_comanda):
        pagamentos = []
        for p in self.pagamentos.listar():
            if p.numero_comanda == numero_comanda:
                pagamentos.append(p)
        return pagamentos

    def buscar_pagamentos_por_cliente(self, cliente):
        pagamentos = []
        for p in self.pagamentos.listar():
            if p.cliente == cliente:
                pagamentos.append(p)
        return pagamentos

    def listar_todos_pagamentos(self):
        return self.pagamentos.listar()


