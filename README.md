# 🏦 NewBank - Sistema Bancário para Testes de Software

Este repositório abriga o desenvolvimento de um sistema bancário criado como parte da disciplina de **Teste de Software**, do curso de **Tecnologia em Sistemas para Internet**.

O projeto tem como foco a aplicação prática de conceitos de **TDD (Test Driven Development)**, testes unitários e validação de regras de negócio em um contexto bancário.

## 👨‍💻 Integrantes do Grupo

- Cezarino Martins da Hora
- Carina Monia da Silva
- Luis Felipe de Souza Nunes
- Guilherme da Silva Guia
- Gabriel Santana Morais

## 📚 Informações do Projeto

- **Disciplina:** Teste de Software
- **Atividade:** Atividade Prática TDD
- **Professor:** Orlando Pereira Santana Junior

## Estrutura do projeto

```text
banco/
├── app.py              # Aplicação Flask (API + UI)
├── conta.py            # Classe ContaBancaria
├── extrato.py          # Classe Extrato e Transacao
├── transferencia.py    # Classe Transferencia
├── juros.py            # Classe CalculadoraJuros
├── templates/
│   └── index.html      # Interface web
└── tests/
    ├── __init__.py
    ├── test_conta.py
    ├── test_extrato.py
    ├── test_transferencia.py
    ├── test_juros.py
    └── test_app.py
```

## Pré-requisitos

- Python 3.8+
- pip

## Instalação

### Windows (Git Bash / MINGW64)

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Como rodar a aplicação

Com o ambiente virtual ativado, inicie o servidor Flask:

```bash
python -m banco.app
```

Acesse a interface web em: **http://127.0.0.1:5000**

### Endpoints disponíveis

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Interface web |
| POST | `/api/conta` | Criar conta |
| GET | `/api/conta/<numero>` | Consultar saldo |
| POST | `/api/conta/<numero>/depositar` | Depositar |
| POST | `/api/conta/<numero>/sacar` | Sacar |
| POST | `/api/transferencia` | Transferir entre contas |
| GET | `/api/extrato/<numero>` | Consultar extrato |
| POST | `/api/extrato/<numero>/transacao` | Adicionar transação |
| POST | `/api/juros/simples` | Calcular juros simples |
| POST | `/api/juros/compostos` | Calcular juros compostos |

## Como rodar os testes

```bash
python -m pytest banco/tests/ -v
```

## O ciclo Red-Green-Refactor

| Fase | Cor         | O que fazer                                                 |
| ---- | ----------- | ----------------------------------------------------------- |
| 1    | 🔴 Red      | Escrever um teste que **falha** (o código ainda não existe) |
| 2    | 🟢 Green    | Escrever o **mínimo** de código para o teste passar         |
| 3    | 🔵 Refactor | Melhorar o código sem quebrar o teste                       |

> Regra de ouro: nunca escreva código de produção sem antes ter um teste falhando.

## Funcionalidades Propostas (Etapa 1: Levantamento de Requisitos)

### Classe ContaBancaria (5 métodos)

- [x] **init**(saldo_inicial=0, numero_conta=None) — Criar conta com saldo inicial e número da conta
- [x] depositar(valor) — Adicionar dinheiro à conta
- [x] sacar(valor) — Remover dinheiro da conta
- [x] getSaldo() — Retornar saldo atual
- [x] getNumeroConta() — Retornar número da conta

### Classe Transferencia (4 métodos)

- [ ] executar() — Executar transferência entre contas
- [ ] getContaOrigem() — Obter conta de origem
- [ ] getContaDestino() — Obter conta de destino
- [ ] getValorTransacao() — Obter valor transferido

### Classe CalculadoraJuros (4 métodos)

- [ ] calcularJurosSimples() — Calcular juros simples
- [ ] calcularJurosCompostos() — Calcular juros compostos
- [ ] getTaxa() — Retornar taxa de juros
- [ ] setTaxa(novaTaxa) — Definir nova taxa de juros

### Classe Extrato (4 métodos)

- [ ] adicionarTransacao() — Registrar uma transação
- [ ] getTransacoes() — Listar todas as transações
- [ ] calcularTotalEntradas() — Somar depósitos
- [ ] calcularTotalSaidas() — Somar saques

## Regras de Negócio Críticas

- [ ] Saldo nunca pode ficar negativo após saque
- [ ] Não aceitar depósitos com valores negativos
- [ ] Transferência requer saldo suficiente na conta origem

## Referências

- [Documentação do pytest](https://docs.pytest.org/)
- [Test-Driven Development by Example — Kent Beck](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530)
