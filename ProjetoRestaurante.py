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


# === PARTE 6: RELATÓRIOS ===

class GeradorRelatorios:
    @staticmethod
    def relatorio_vendas(restaurante):
        pagamentos = restaurante.gerenciador_pagamentos.listar_todos_pagamentos()

        if not pagamentos:
            print("Nenhuma venda registrada.")
            return

        print("=== RELATÓRIO DE VENDAS ===")
        print(f"Total de vendas: {len(pagamentos)} transações")

        valor_total = sum(p.valor for p in pagamentos)
        print(f"Valor total arrecadado: R$ {valor_total:.2f}")
        print()

        # Por forma de pagamento
        print("--- Por Forma de Pagamento ---")
        formas = {}
        for p in pagamentos:
            formas[p.forma_pagamento] = formas.get(p.forma_pagamento, 0) + p.valor
        for forma, valor in formas.items():
            print(f"{forma}: R$ {valor:.2f} ({valor/valor_total*100:.1f}%)")
        print()

        # Por cliente
        print("--- Por Cliente ---")
        clientes = {}
        for p in pagamentos:
            clientes[p.cliente] = clientes.get(p.cliente, 0) + p.valor
        for cliente, valor in sorted(clientes.items(), key=lambda x: x[1], reverse=True):
            print(f"{cliente}: R$ {valor:.2f}")
        print()

        # Detalhamento por comanda
        print("--- Detalhamento por Comanda ---")
        for p in pagamentos:
            print(f"Comanda {p.numero_comanda}: {p.cliente} - R$ {p.valor:.2f} ({p.forma_pagamento}) - {p.data_hora.strftime('%d/%m/%Y %H:%M')}")

    @staticmethod
    def relatorio_consumo(restaurante):
        consumos = restaurante.gerenciador_consumo.listar_todos_consumos()

        if not consumos:
            print("Nenhum consumo registrado.")
            return

        print("=== RELATÓRIO DE CONSUMO ===")
        print(f"Total de itens consumidos: {len(consumos)}")
        print()

        # Por cliente
        print("--- Por Cliente ---")
        clientes = {}
        for c in consumos:
            clientes[c.cliente] = clientes.get(c.cliente, 0) + c.quantidade
        for cliente, qtd in sorted(clientes.items(), key=lambda x: x[1], reverse=True):
            print(f"{cliente}: {qtd} itens")
        print()

        # Por produto
        print("--- Por Produto ---")
        produtos = {}
        for c in consumos:
            produtos[c.item_nome] = produtos.get(c.item_nome, 0) + c.quantidade
        for produto, qtd in sorted(produtos.items(), key=lambda x: x[1], reverse=True):
            print(f"{produto}: {qtd} unidades")
        print()

        # Detalhamento
        print("--- Detalhamento Completo ---")
        for c in consumos:
            print(f"{c.cliente} - Comanda {c.comanda_numero}: {c.item_nome} (Qtd: {c.quantidade}) - {c.data_hora.strftime('%d/%m/%Y %H:%M')}")

    @staticmethod
    def relatorio_estoque(restaurante):
        produtos = restaurante.gerenciador_estoque.listar_estoque()

        if not produtos:
            print("Estoque vazio.")
            return

        print("=== RELATÓRIO DE ESTOQUE ===")
        print(f"Total de produtos: {len(produtos)}")
        print()

        valor_total_estoque = sum(p.quantidade * p.preco_compra for p in produtos)
        print(f"Valor total do estoque (compra): R$ {valor_total_estoque:.2f}")
        print()

        print("--- Produtos em Estoque ---")
        for p in produtos:
            print(f"{p.nome}: {p.quantidade} unidades | Compra: R$ {p.preco_compra:.2f} | Venda: R$ {p.preco_venda:.2f} | Vence: {p.data_vencimento.strftime('%d/%m/%Y')}")


# === TESTE DO SISTEMA INTEGRADO ===
if __name__ == "__main__":
    # === TESTE 1: Dados aleatórios com Faker ===
    print("=== TESTE 1: DADOS ALEATÓRIOS COM FAKER ===")
    restaurante = Restaurante()
    gerador = GeradorDados()

    # Popular estoque com dados aleatórios
    print("=== POPULANDO ESTOQUE COM DADOS ALEATÓRIOS ===")
    gerador.popular_estoque_aleatorio(restaurante.gerenciador_estoque, quantidade_produtos=8)

    print("=== ESTOQUE ALEATÓRIO ===")
    for produto in restaurante.gerenciador_estoque.listar_estoque():
        print(f"{produto.nome}: {produto.quantidade} unidades (R$ {produto.preco_venda:.2f})")
    print()

    # Simular múltiplos atendimentos aleatórios
    print("=== SIMULANDO ATENDIMENTOS ALEATÓRIOS ===")
    for i in range(3):
        comanda = gerador.gerar_atendimento_completo(restaurante)
        print(f"Atendimento {i+1}: Comanda {comanda.numero} - {comanda.cliente} - Total: R$ {comanda.total():.2f}")
    print()

    # === TESTE 2: Persistência com Pickle ===
    print("=== TESTE 2: PERSISTÊNCIA COM PICKLE ===")
    PersistenciaDados.salvar_restaurante(restaurante, 'restaurante_teste.pkl')

    restaurante_carregado = PersistenciaDados.carregar_restaurante('restaurante_teste.pkl')
    if restaurante_carregado:
        print("=== DADOS CARREGADOS COM SUCESSO ===")
        print(f"Comandas no sistema: {len(restaurante_carregado.gerenciador_comandas.comandas.listar())}")
        print(f"Produtos em estoque: {len(restaurante_carregado.gerenciador_estoque.listar_estoque())}")
        print(f"Pagamentos registrados: {len(restaurante_carregado.gerenciador_pagamentos.listar_todos_pagamentos())}")
        print(f"Registros de consumo: {len(restaurante_carregado.gerenciador_consumo.listar_todos_consumos())}")
        print()

    # === TESTE 3: Relatórios ===
    print("=== TESTE 3: RELATÓRIOS ===")
    GeradorRelatorios.relatorio_vendas(restaurante)
    print()
    GeradorRelatorios.relatorio_consumo(restaurante)
    print()
    GeradorRelatorios.relatorio_estoque(restaurante)
