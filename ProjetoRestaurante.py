from datetime import datetime, timedelta
import pickle
from faker import Faker


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


# === PARTE 4: CONTROLE DO QUE CONSUMIU ===

class Consumo:
    def __init__(self, cliente, comanda_numero, item_nome, quantidade, data_hora):
        self.cliente = cliente
        self.comanda_numero = comanda_numero
        self.item_nome = item_nome
        self.quantidade = quantidade
        self.data_hora = data_hora


class GerenciadorConsumo:
    def __init__(self):
        self.consumos = ListaEncadeada()

    def registrar_consumo(self, consumo):
        self.consumos.adicionar(consumo)

    def buscar_consumo_por_cliente(self, cliente):
        consumos = []
        for c in self.consumos.listar():
            if c.cliente == cliente:
                consumos.append(c)
        return consumos

    def buscar_consumo_por_comanda(self, numero_comanda):
        consumos = []
        for c in self.consumos.listar():
            if c.comanda_numero == numero_comanda:
                consumos.append(c)
        return consumos

    def listar_todos_consumos(self):
        return self.consumos.listar()


# === SISTEMA INTEGRADO DO RESTAURANTE ===

class Restaurante:
    def __init__(self):
        self.gerenciador_comandas = GerenciadorComandas()
        self.gerenciador_estoque = GerenciadorEstoque()
        self.gerenciador_pagamentos = GerenciadorPagamentos()
        self.gerenciador_consumo = GerenciadorConsumo()

    def abrir_comanda(self, cliente):
        return self.gerenciador_comandas.abrir(cliente)

    def adicionar_item_comanda(self, numero_comanda, item):
        comanda = self.gerenciador_comandas.buscar(numero_comanda)
        if comanda and not comanda.fechada:
            comanda.adicionar_item(item)
            return True
        return False

    def remover_item_comanda(self, numero_comanda, item):
        comanda = self.gerenciador_comandas.buscar(numero_comanda)
        if comanda and not comanda.fechada:
            return comanda.remover_item(item)
        return False

    def fechar_comanda_e_pagar(self, numero_comanda, forma_pagamento):
        comanda = self.gerenciador_comandas.buscar(numero_comanda)
        if not comanda or comanda.fechada:
            return False

        # Baixar estoque dos produtos consumidos
        for item in comanda.refeicoes.listar():
            self._baixar_estoque(item.nome, 1)
            consumo = Consumo(comanda.cliente, comanda.numero, item.nome, 1, datetime.now())
            self.gerenciador_consumo.registrar_consumo(consumo)

        for item in comanda.bebidas.listar():
            self._baixar_estoque(item.nome, 1)
            consumo = Consumo(comanda.cliente, comanda.numero, item.nome, 1, datetime.now())
            self.gerenciador_consumo.registrar_consumo(consumo)

        # Registrar pagamento
        valor_total = comanda.total()
        pagamento = Pagamento(comanda.cliente, comanda.numero, forma_pagamento, valor_total, datetime.now())
        self.gerenciador_pagamentos.registrar_pagamento(pagamento)

        # Fechar comanda
        comanda.fechar()
        return True

    def _baixar_estoque(self, nome_produto, quantidade):
        produto = self.gerenciador_estoque.buscar_produto(nome_produto)
        if produto:
            nova_qtd = max(0, produto.quantidade - quantidade)
            self.gerenciador_estoque.editar_quantidade(nome_produto, nova_qtd)


# === PARTE 5: GERAÇÃO E ARMAZENAMENTO DE DADOS ===

class GeradorDados:
    def __init__(self):
        self.faker = Faker('pt_BR')

    def gerar_nome_cliente(self):
        return self.faker.name()

    def gerar_produto_aleatorio(self):
        nomes_produtos = ["Hambúrguer", "Pizza", "Batata Frita", "Coca Cola", "Suco", "Água", "Refrigerante", "Salada"]
        nome = self.faker.random_element(nomes_produtos)
        tipo = "bebida" if nome in ["Coca Cola", "Suco", "Água", "Refrigerante"] else "refeicao"
        preco_compra = round(self.faker.random.uniform(2.0, 15.0), 2)
        preco_venda = round(preco_compra * self.faker.random.uniform(2.0, 3.0), 2)
        data_compra = self.faker.date_between(start_date='-30d', end_date='today')
        data_vencimento = data_compra + timedelta(days=self.faker.random_int(7, 60))
        quantidade = self.faker.random_int(10, 100)
        return Produto(nome, preco_compra, preco_venda, data_compra, data_vencimento, quantidade)

    def popular_estoque_aleatorio(self, gerenciador_estoque, quantidade_produtos=10):
        for _ in range(quantidade_produtos):
            produto = self.gerar_produto_aleatorio()
            gerenciador_estoque.adicionar_produto(produto)

    def gerar_atendimento_completo(self, restaurante):
        cliente = self.gerar_nome_cliente()
        comanda = restaurante.abrir_comanda(cliente)

        # Adicionar refeições aleatórias
        num_refeicoes = self.faker.random_int(1, 3)
        refeicoes_disponiveis = ["Hambúrguer", "Pizza", "Batata Frita", "Salada"]
        for _ in range(num_refeicoes):
            nome = self.faker.random_element(refeicoes_disponiveis)
            preco = round(self.faker.random.uniform(15.0, 40.0), 2)
            restaurante.adicionar_item_comanda(comanda.numero, Item(nome, preco, "refeicao"))

        # Adicionar bebidas aleatórias
        num_bebidas = self.faker.random_int(1, 2)
        bebidas_disponiveis = ["Coca Cola", "Suco", "Água"]
        for _ in range(num_bebidas):
            nome = self.faker.random_element(bebidas_disponiveis)
            preco = round(self.faker.random.uniform(4.0, 10.0), 2)
            restaurante.adicionar_item_comanda(comanda.numero, Item(nome, preco, "bebida"))

        # Fechar comanda e pagar
        formas_pagamento = ["PIX", "cartao", "dinheiro"]
        forma = self.faker.random_element(formas_pagamento)
        restaurante.fechar_comanda_e_pagar(comanda.numero, forma)

        return comanda


class PersistenciaDados:
    @staticmethod
    def salvar_restaurante(restaurante, arquivo='restaurante_data.pkl'):
        with open(arquivo, 'wb') as f:
            pickle.dump(restaurante, f)
        print(f"Dados salvos em {arquivo}")

    @staticmethod
    def carregar_restaurante(arquivo='restaurante_data.pkl'):
        try:
            with open(arquivo, 'rb') as f:
                restaurante = pickle.load(f)
            print(f"Dados carregados de {arquivo}")
            return restaurante
        except FileNotFoundError:
            print(f"Arquivo {arquivo} não encontrado")
            return None
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return None


# === TESTE DO SISTEMA INTEGRADO ===
if __name__ == "__main__":
    # === TESTE 1: Manual (original) ===
    print("=== TESTE 1: DADOS MANUAIS ===")
    restaurante = Restaurante()

    # Popular estoque inicial
    hoje = datetime.now()
    restaurante.gerenciador_estoque.adicionar_produto(
        Produto("Hambúrguer", 10.00, 25.00, hoje, hoje + timedelta(days=7), 20)
    )
    restaurante.gerenciador_estoque.adicionar_produto(
        Produto("Batata Frita", 5.00, 15.00, hoje, hoje + timedelta(days=10), 30)
    )
    restaurante.gerenciador_estoque.adicionar_produto(
        Produto("Coca Cola", 3.00, 8.00, hoje, hoje + timedelta(days=30), 50)
    )
    restaurante.gerenciador_estoque.adicionar_produto(
        Produto("Suco", 2.00, 6.00, hoje, hoje + timedelta(days=15), 40)
    )
    restaurante.gerenciador_estoque.adicionar_produto(
        Produto("Água", 1.00, 4.00, hoje, hoje + timedelta(days=60), 100)
    )

    print("=== ESTOQUE INICIAL ===")
    for produto in restaurante.gerenciador_estoque.listar_estoque():
        print(f"{produto.nome}: {produto.quantidade} unidades (R$ {produto.preco_venda:.2f})")
    print()

    # Simular atendimento completo
    print("=== ATENDIMENTO COMPLETO ===")
    comanda1 = restaurante.abrir_comanda("João")
    print(f"Comanda aberta: {comanda1.numero} - Cliente: {comanda1.cliente}")

    restaurante.adicionar_item_comanda(comanda1.numero, Item("Hambúrguer", 25.00, "refeicao"))
    restaurante.adicionar_item_comanda(comanda1.numero, Item("Batata Frita", 15.00, "refeicao"))
    restaurante.adicionar_item_comanda(comanda1.numero, Item("Coca Cola", 8.00, "bebida"))
    print(f"Itens adicionados à comanda {comanda1.numero}")

    print(f"Total da comanda: R$ {comanda1.total():.2f}")
    print()

    # Fechar comanda e pagar
    restaurante.fechar_comanda_e_pagar(comanda1.numero, "cartao")
    print(f"Comanda {comanda1.numero} fechada e paga com cartão")
    print()

    # Verificar estoque após consumo
    print("=== ESTOQUE APÓS CONSUMO ===")
    for produto in restaurante.gerenciador_estoque.listar_estoque():
        print(f"{produto.nome}: {produto.quantidade} unidades")
    print()

    # Verificar registros
    print("=== REGISTRO DE CONSUMO ===")
    for consumo in restaurante.gerenciador_consumo.buscar_consumo_por_comanda(comanda1.numero):
        print(f"{consumo.cliente} consumiu: {consumo.item_nome} (Qtd: {consumo.quantidade})")
    print()

    print("=== REGISTRO DE PAGAMENTO ===")
    for pagamento in restaurante.gerenciador_pagamentos.buscar_pagamentos_por_comanda(comanda1.numero):
        print(f"{pagamento.cliente} pagou R$ {pagamento.valor:.2f} via {pagamento.forma_pagamento}")
    print()

    # === TESTE 2: Faker (dados aleatórios) ===
    print("\n=== TESTE 2: DADOS ALEATÓRIOS COM FAKER ===")
    restaurante_faker = Restaurante()
    gerador = GeradorDados()

    # Popular estoque com dados aleatórios
    print("=== POPULANDO ESTOQUE COM DADOS ALEATÓRIOS ===")
    gerador.popular_estoque_aleatorio(restaurante_faker.gerenciador_estoque, quantidade_produtos=8)

    print("=== ESTOQUE ALEATÓRIO ===")
    for produto in restaurante_faker.gerenciador_estoque.listar_estoque():
        print(f"{produto.nome}: {produto.quantidade} unidades (R$ {produto.preco_venda:.2f})")
    print()

    # Simular múltiplos atendimentos aleatórios
    print("=== SIMULANDO ATENDIMENTOS ALEATÓRIOS ===")
    for i in range(3):
        comanda = gerador.gerar_atendimento_completo(restaurante_faker)
        print(f"Atendimento {i+1}: Comanda {comanda.numero} - {comanda.cliente} - Total: R$ {comanda.total():.2f}")
    print()

    # === TESTE 3: Persistência com Pickle ===
    print("=== TESTE 3: PERSISTÊNCIA COM PICKLE ===")
    PersistenciaDados.salvar_restaurante(restaurante_faker, 'restaurante_teste.pkl')

    restaurante_carregado = PersistenciaDados.carregar_restaurante('restaurante_teste.pkl')
    if restaurante_carregado:
        print("=== DADOS CARREGADOS COM SUCESSO ===")
        print(f"Comandas no sistema: {len(restaurante_carregado.gerenciador_comandas.comandas.listar())}")
        print(f"Produtos em estoque: {len(restaurante_carregado.gerenciador_estoque.listar_estoque())}")
        print(f"Pagamentos registrados: {len(restaurante_carregado.gerenciador_pagamentos.listar_todos_pagamentos())}")
        print(f"Registros de consumo: {len(restaurante_carregado.gerenciador_consumo.listar_todos_consumos())}")
