import pytest
from banco.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ── Menu principal ────────────────────────────────────────────────────────────

def test_menu_retorna_html(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"text/html" in response.content_type.encode()


# ── Conta ─────────────────────────────────────────────────────────────────────

def test_criar_conta(client):
    response = client.post("/api/conta", json={"numero": "001", "saldo_inicial": 500.0})
    assert response.status_code == 201
    data = response.get_json()
    assert data["numero"] == "001"
    assert data["saldo"] == 500.0


def test_criar_conta_duplicada_retorna_erro(client):
    client.post("/api/conta", json={"numero": "001", "saldo_inicial": 100.0})
    response = client.post("/api/conta", json={"numero": "001", "saldo_inicial": 200.0})
    assert response.status_code == 409


def test_criar_conta_sem_numero_retorna_erro(client):
    response = client.post("/api/conta", json={"saldo_inicial": 100.0})
    assert response.status_code == 400


def test_consultar_saldo(client):
    client.post("/api/conta", json={"numero": "001", "saldo_inicial": 300.0})
    response = client.get("/api/conta/001")
    assert response.status_code == 200
    assert response.get_json()["saldo"] == 300.0


def test_consultar_conta_inexistente_retorna_404(client):
    response = client.get("/api/conta/999")
    assert response.status_code == 404


def test_depositar_em_conta(client):
    client.post("/api/conta", json={"numero": "001", "saldo_inicial": 100.0})
    response = client.post("/api/conta/001/depositar", json={"valor": 50.0})
    assert response.status_code == 200
    assert response.get_json()["saldo"] == 150.0


def test_depositar_valor_negativo_retorna_erro(client):
    client.post("/api/conta", json={"numero": "001", "saldo_inicial": 100.0})
    response = client.post("/api/conta/001/depositar", json={"valor": -50.0})
    assert response.status_code == 400


def test_depositar_sem_valor_retorna_erro(client):
    client.post("/api/conta", json={"numero": "001"})
    response = client.post("/api/conta/001/depositar", json={})
    assert response.status_code == 400


def test_sacar_de_conta(client):
    client.post("/api/conta", json={"numero": "001", "saldo_inicial": 200.0})
    response = client.post("/api/conta/001/sacar", json={"valor": 80.0})
    assert response.status_code == 200
    assert response.get_json()["saldo"] == 120.0


def test_sacar_saldo_insuficiente_retorna_erro(client):
    client.post("/api/conta", json={"numero": "001", "saldo_inicial": 50.0})
    response = client.post("/api/conta/001/sacar", json={"valor": 200.0})
    assert response.status_code == 422


# ── Transferência ─────────────────────────────────────────────────────────────

def test_transferencia_entre_contas(client):
    client.post("/api/conta", json={"numero": "001", "saldo_inicial": 1000.0})
    client.post("/api/conta", json={"numero": "002", "saldo_inicial": 500.0})
    response = client.post("/api/transferencia", json={
        "conta_origem": "001",
        "conta_destino": "002",
        "valor": 300.0
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["conta_origem"]["saldo"] == 700.0
    assert data["conta_destino"]["saldo"] == 800.0


def test_transferencia_saldo_insuficiente_retorna_erro(client):
    client.post("/api/conta", json={"numero": "001", "saldo_inicial": 100.0})
    client.post("/api/conta", json={"numero": "002", "saldo_inicial": 500.0})
    response = client.post("/api/transferencia", json={
        "conta_origem": "001",
        "conta_destino": "002",
        "valor": 999.0
    })
    assert response.status_code == 422


def test_transferencia_mesma_conta_retorna_erro(client):
    client.post("/api/conta", json={"numero": "001", "saldo_inicial": 1000.0})
    response = client.post("/api/transferencia", json={
        "conta_origem": "001",
        "conta_destino": "001",
        "valor": 100.0
    })
    assert response.status_code == 400


# ── Extrato ───────────────────────────────────────────────────────────────────

def test_extrato_vazio(client):
    client.post("/api/conta", json={"numero": "001", "saldo_inicial": 0})
    response = client.get("/api/extrato/001")
    assert response.status_code == 200
    data = response.get_json()
    assert data["transacoes"] == []
    assert data["total_entradas"] == 0
    assert data["total_saidas"] == 0


def test_adicionar_transacao_ao_extrato(client):
    client.post("/api/conta", json={"numero": "001", "saldo_inicial": 0})
    response = client.post("/api/extrato/001/transacao", json={
        "valor": 200.0,
        "categoria": "deposito",
        "responsavel": "Maria"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert len(data["transacoes"]) == 1


def test_adicionar_transacao_com_categoria_invalida_retorna_erro(client):
    client.post("/api/conta", json={"numero": "001"})
    response = client.post("/api/extrato/001/transacao", json={
        "valor": 200.0,
        "categoria": "invalida",
    })
    assert response.status_code == 400


def test_extrato_calcula_totais(client):
    client.post("/api/conta", json={"numero": "001", "saldo_inicial": 100.0})
    client.post("/api/extrato/001/transacao", json={"valor": 300.0, "categoria": "deposito", "responsavel": "Ana"})
    client.post("/api/extrato/001/transacao", json={"valor": 100.0, "categoria": "saque", "responsavel": "Ana"})
    response = client.get("/api/extrato/001")
    data = response.get_json()
    assert data["total_entradas"] == 400.0  # 100 saldo inicial + 300 depósito manual
    assert data["total_saidas"] == 100.0


# ── Juros ─────────────────────────────────────────────────────────────────────

def test_calcular_juros_simples(client):
    response = client.post("/api/juros/simples", json={"capital": 1000.0, "taxa": 0.1, "tempo": 2})
    assert response.status_code == 200
    assert response.get_json()["montante"] == pytest.approx(1200.0)


def test_calcular_juros_compostos(client):
    response = client.post("/api/juros/compostos", json={"capital": 1000.0, "taxa": 0.1, "tempo": 2})
    assert response.status_code == 200
    assert response.get_json()["montante"] == pytest.approx(1210.0)


def test_calcular_juros_taxa_negativa_retorna_erro(client):
    response = client.post("/api/juros/simples", json={"capital": 1000.0, "taxa": -0.1, "tempo": 2})
    assert response.status_code == 400


def test_calcular_juros_sem_capital_retorna_erro(client):
    response = client.post("/api/juros/simples", json={"taxa": 0.1, "tempo": 2})
    assert response.status_code == 400
