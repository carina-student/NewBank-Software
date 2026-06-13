import os
from flask import Flask, jsonify, request, render_template
from banco.conta import ContaBancaria, SaldoInsuficienteException
from banco.extrato import Extrato, Transacao, CategoriaTransacao
from banco.transferencia import Transferencia
from banco.juros import CalculadoraJuros
from datetime import datetime


def create_app():
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    app = Flask(__name__, template_folder=template_dir)

    contas: dict[str, ContaBancaria] = {}
    extratos: dict[str, Extrato] = {}

    def obter_body():
        body = request.get_json(silent=True)
        if not isinstance(body, dict):
            raise ValueError("Corpo JSON inválido")
        return body

    @app.errorhandler(ValueError)
    def tratar_value_error(error):
        return jsonify({"erro": str(error)}), 400

    @app.errorhandler(SaldoInsuficienteException)
    def tratar_saldo_insuficiente(error):
        return jsonify({"erro": str(error)}), 422

    # ── Menu ──────────────────────────────────────────────────────────────────

    @app.route("/")
    def menu():
        return render_template("index.html"), 200

    # ── Conta ─────────────────────────────────────────────────────────────────

    @app.route("/api/conta", methods=["POST"])
    def criar_conta():
        body = obter_body()
        numero = body.get("numero")
        saldo_inicial = body.get("saldo_inicial", 0)

        if not isinstance(numero, str) or not numero.strip():
            raise ValueError("Número da conta é obrigatório")
        numero = numero.strip()

        if numero in contas:
            return jsonify({"erro": "Conta já existe"}), 409

        contas[numero] = ContaBancaria(saldo_inicial=saldo_inicial, numero_conta=numero)
        extratos[numero] = Extrato()

        if saldo_inicial and saldo_inicial > 0:
            extratos[numero].adicionar_transacao(Transacao(
                valor=saldo_inicial,
                categoria=CategoriaTransacao.DEPOSITO,
                data_operacao=datetime.now(),
                responsavel="Saldo inicial",
            ))

        return jsonify({"numero": numero, "saldo": contas[numero].getSaldo()}), 201

    @app.route("/api/conta/<numero>", methods=["GET"])
    def consultar_conta(numero):
        if numero not in contas:
            return jsonify({"erro": "Conta não encontrada"}), 404
        return jsonify({"numero": numero, "saldo": contas[numero].getSaldo()}), 200

    @app.route("/api/conta/<numero>/depositar", methods=["POST"])
    def depositar(numero):
        if numero not in contas:
            return jsonify({"erro": "Conta não encontrada"}), 404
        body = obter_body()
        try:
            valor = body.get("valor")
            contas[numero].depositar(valor)
            extratos[numero].adicionar_transacao(Transacao(
                valor=valor,
                categoria=CategoriaTransacao.DEPOSITO,
                data_operacao=datetime.now(),
                responsavel="Sistema",
            ))
            return jsonify({"numero": numero, "saldo": contas[numero].getSaldo()}), 200
        except ValueError as e:
            return jsonify({"erro": str(e)}), 400

    @app.route("/api/conta/<numero>/sacar", methods=["POST"])
    def sacar(numero):
        if numero not in contas:
            return jsonify({"erro": "Conta não encontrada"}), 404
        body = obter_body()
        try:
            valor = body.get("valor")
            contas[numero].sacar(valor)
            extratos[numero].adicionar_transacao(Transacao(
                valor=valor,
                categoria=CategoriaTransacao.SAQUE,
                data_operacao=datetime.now(),
                responsavel="Sistema",
            ))
            return jsonify({"numero": numero, "saldo": contas[numero].getSaldo()}), 200
        except SaldoInsuficienteException as e:
            return jsonify({"erro": str(e)}), 422
        except ValueError as e:
            return jsonify({"erro": str(e)}), 400

    # ── Transferência ─────────────────────────────────────────────────────────

    @app.route("/api/transferencia", methods=["POST"])
    def transferencia():
        body = obter_body()
        num_origem = body.get("conta_origem")
        num_destino = body.get("conta_destino")
        valor = body.get("valor")

        if num_origem not in contas or num_destino not in contas:
            return jsonify({"erro": "Conta não encontrada"}), 404

        try:
            t = Transferencia(contas[num_origem], contas[num_destino], valor)
            t.executar()
            agora = datetime.now()
            extratos[num_origem].adicionar_transacao(Transacao(
                valor=valor,
                categoria=CategoriaTransacao.SAQUE,
                data_operacao=agora,
                responsavel=f"Transferência para {num_destino}",
            ))
            extratos[num_destino].adicionar_transacao(Transacao(
                valor=valor,
                categoria=CategoriaTransacao.DEPOSITO,
                data_operacao=agora,
                responsavel=f"Transferência de {num_origem}",
            ))
            return jsonify({
                "conta_origem": {"numero": num_origem, "saldo": contas[num_origem].getSaldo()},
                "conta_destino": {"numero": num_destino, "saldo": contas[num_destino].getSaldo()},
            }), 200
        except SaldoInsuficienteException as e:
            return jsonify({"erro": str(e)}), 422
        except ValueError as e:
            return jsonify({"erro": str(e)}), 400

    # ── Extrato ───────────────────────────────────────────────────────────────

    @app.route("/api/extrato/<numero>", methods=["GET"])
    def extrato(numero):
        if numero not in extratos:
            return jsonify({"erro": "Conta não encontrada"}), 404
        ext = extratos[numero]
        transacoes = [
            {
                "valor": t.valor,
                "categoria": t.categoria.value,
                "responsavel": t.responsavel,
                "data": t.data_operacao.strftime("%d/%m/%Y %H:%M"),
            }
            for t in ext.getTransacoes()
        ]
        return jsonify({
            "transacoes": transacoes,
            "total_entradas": ext.calcularTotalEntradas(),
            "total_saidas": ext.calcularTotalSaidas(),
        }), 200

    @app.route("/api/extrato/<numero>/transacao", methods=["POST"])
    def adicionar_transacao(numero):
        if numero not in extratos:
            return jsonify({"erro": "Conta não encontrada"}), 404
        body = obter_body()
        categoria_str = body.get("categoria")
        try:
            categoria = CategoriaTransacao(categoria_str)
        except (TypeError, ValueError):
            raise ValueError("Categoria deve ser 'deposito' ou 'saque'")
        try:
            t = Transacao(
                valor=body.get("valor"),
                categoria=categoria,
                data_operacao=datetime.now(),
                responsavel=body.get("responsavel"),
            )
            extratos[numero].adicionar_transacao(t)
            transacoes = [
                {"valor": tx.valor, "categoria": tx.categoria.value, "responsavel": tx.responsavel}
                for tx in extratos[numero].getTransacoes()
            ]
            return jsonify({"transacoes": transacoes}), 201
        except ValueError as e:
            return jsonify({"erro": str(e)}), 400

    # ── Juros ─────────────────────────────────────────────────────────────────

    @app.route("/api/juros/simples", methods=["POST"])
    def juros_simples():
        body = obter_body()
        taxa = body.get("taxa", 0)
        calc = CalculadoraJuros(taxa=taxa)
        montante = calc.calcularJurosSimples(body.get("capital"), body.get("tempo"))
        return jsonify({"montante": montante}), 200

    @app.route("/api/juros/compostos", methods=["POST"])
    def juros_compostos():
        body = obter_body()
        taxa = body.get("taxa", 0)
        calc = CalculadoraJuros(taxa=taxa)
        montante = calc.calcularJurosCompostos(body.get("capital"), body.get("tempo"))
        return jsonify({"montante": montante}), 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
