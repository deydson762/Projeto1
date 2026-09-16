# Projeto de Avaliação — Estrutura de Dados

## 📚 Sobre o Projeto

Este projeto foi desenvolvido como parte da avaliação da disciplina de Estrutura de Dados, tendo como tema principal o gerenciamento de um restaurante. O objetivo é aplicar, na prática, os conceitos estudados durante as aulas, utilizando estruturas de dados e técnicas de programação para desenvolver uma solução funcional que represente situações do dia a dia de um restaurante.

Durante o desenvolvimento, serão utilizados conceitos como listas, pilhas, filas, estruturas encadeadas, busca, ordenação e outros conteúdos relacionados à disciplina, aplicados ao gerenciamento de informações e processos do restaurante.

## 🎯 Objetivos

* Desenvolver um sistema para gerenciamento de um restaurante;
* Criar uma estrutura para controle das comandas abertas;
* Gerenciar refeições e bebidas adicionadas às comandas;
* Controlar o estoque de produtos, considerando validade e prioridade dos produtos mais antigos;
* Permitir a edição da quantidade de produtos em estoque;
* Gerenciar os pagamentos realizados no fechamento das comandas;
* Controlar o consumo e realizar a baixa dos produtos utilizados no estoque;
* Gerar relatórios de vendas e consumo;
* Aplicar conceitos de Estrutura de Dados e Programação Orientada a Objetos na solução.

## 🛠️ Tecnologias e Bibliotecas Utilizadas

* **Python**
* **Git**
* **GitHub**
* **Faker** — geração de dados aleatórios para popular o sistema;
* **Pickle** — armazenamento e carregamento dos dados de forma não volátil.

## 🧩 Estruturas de Dados e Classes

O projeto deverá utilizar **classes próprias** para implementar as estruturas de dados necessárias, separando as responsabilidades de cada parte do sistema.

Os principais módulos e estruturas do projeto envolvem:

* **Controle de Comandas** — número da comanda, cliente, data e hora de abertura, refeições e bebidas;
* **Controle de Estoque** — produtos, preços, datas de compra e vencimento e quantidade disponível;
* **Controle de Pagamentos** — cliente, comanda, forma de pagamento, valor, data e hora;
* **Controle de Consumo** — registro dos itens consumidos e baixa dos produtos utilizados no estoque;
* **Geração e armazenamento de dados** — utilização das bibliotecas Faker e pickle;
* **Relatórios** — geração de relatórios de vendas e consumo.

As estruturas de dados devem ser implementadas por meio de **classes próprias**, evitando o uso direto de estruturas built-in do Python para solucionar os problemas propostos.

## 👨‍🏫 Disciplinas

**Estrutura de Dados** / **Linguagem de Programação 2**

**Instituição:** Fatec Rio Claro

## 📌 Status do Projeto

✅ **Concluído**

O projeto foi desenvolvido por meio de **entregas incrementais no GitHub**, conforme os requisitos da avaliação.

**Prazo final:** 17/09/2026
**Apresentação:** 07h50

O sistema simula um atendimento completo, desde a abertura da comanda e inclusão dos itens até o fechamento e pagamento.

## 🚀 Como Executar

1. Certifique-se de ter Python instalado
2. Instale as dependências:
   ```bash
   pip install faker
   ```
3. Execute o projeto:
   ```bash
   python ProjetoRestaurante.py
   ```

## 📐 Estrutura do Código

O projeto foi implementado utilizando **classes próprias** para estruturas de dados, conforme exigido:

### Estruturas de Dados Base
- **No** - Nó para estruturas encadeadas
- **ListaEncadeada** - Implementação própria de lista encadeada
- **FilaEncadeada** - Implementação própria de fila (FIFO) para produtos perecíveis

### Classes Principais
- **Item** - Representa refeições e bebidas
- **Comanda** - Gerencia uma comanda individual
- **GerenciadorComandas** - Controla todas as comandas do restaurante
- **Produto** - Representa produtos em estoque
- **GerenciadorEstoque** - Gerencia o estoque com fila FIFO
- **Pagamento** - Registra informações de pagamento
- **GerenciadorPagamentos** - Controla todos os pagamentos
- **Consumo** - Registra itens consumidos
- **GerenciadorConsumo** - Gerencia registros de consumo
- **Restaurante** - Classe integradora que conecta todos os módulos
- **GeradorDados** - Gera dados aleatórios usando Faker
- **PersistenciaDados** - Salva/carrega dados usando pickle
- **GeradorRelatorios** - Gera relatórios de vendas, consumo e estoque

## ✅ Funcionalidades Implementadas

1. **Controle de Comandas** - Abertura, adição/remoção de itens, fechamento
2. **Controle de Estoque** - Gerenciamento com prioridade FIFO para produtos perecíveis
3. **Controle de Pagamentos** - Registro via PIX, cartão ou dinheiro
4. **Controle de Consumo** - Baixa automática de estoque e registro de consumo
5. **Geração de Dados** - Dados aleatórios com Faker
6. **Persistência** - Armazenamento não volátil com pickle
7. **Relatórios** - Vendas, consumo e estoque
