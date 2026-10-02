import io
import base64
import qrcode
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from config import Config
from models import db, Item, Presente

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Inicialização opcional do SDK do Mercado Pago
mp_sdk = None
if app.config.get('MERCADO_PAGO_ACCESS_TOKEN'):
    try:
        import mercadopago
        mp_sdk = mercadopago.SDK(app.config['MERCADO_PAGO_ACCESS_TOKEN'])
        print("SDK do Mercado Pago inicializado com sucesso.")
    except Exception as e:
        print(f"Aviso ao carregar SDK do Mercado Pago: {e}")

@app.before_request
def setup_db():
    if not hasattr(app, 'db_initialized'):
        db.create_all()
        # Migration auxiliar para adicionar coluna 'valor' se nao existir na tabela 'presentes'
        try:
            db.session.execute(db.text("SELECT valor FROM presentes LIMIT 1"))
        except Exception:
            db.session.rollback()
            try:
                db.session.execute(db.text("ALTER TABLE presentes ADD COLUMN valor FLOAT DEFAULT 0.0"))
                db.session.commit()
            except Exception as ex:
                print(f"Erro ao adicionar coluna valor: {ex}")
                db.session.rollback()

        # Se não houver itens, executa o seed inicial
        if Item.query.count() == 0:
            from seed import seed_database
            seed_database()
        app.db_initialized = True

# --- ROTAS WEB ---

@app.route('/')
def index():
    categoria_filtro = request.args.get('categoria', 'todas')
    
    if categoria_filtro and categoria_filtro != 'todas':
        itens = Item.query.filter_by(categoria=categoria_filtro).order_by(Item.status.asc(), Item.destaque.desc()).all()
    else:
        itens = Item.query.order_by(Item.status.asc(), Item.destaque.desc()).all()

    # Buscar categorias únicas para os botões de filtro
    categorias_query = db.session.query(Item.categoria).distinct().all()
    categorias = [cat[0] for cat in categorias_query]

    total_itens = Item.query.count()
    total_presenteados = Item.query.filter_by(status='presenteado').count()

    return render_template(
        'index.html',
        itens=itens,
        categorias=categorias,
        categoria_ativa=categoria_filtro,
        total_itens=total_itens,
        total_presenteados=total_presenteados
    )

@app.route('/mural')
def mural():
    presentes_aprovados = Presente.query.filter(
        Presente.status_pagamento == 'approved',
        Presente.mensagem.isnot(None),
        Presente.mensagem != ''
    ).order_by(Presente.created_at.desc()).all()

    return render_template('mural.html', presentes=presentes_aprovados)

@app.route('/confirmacao/<int:presente_id>')
def confirmacao(presente_id):
    presente = Presente.query.get_or_404(presente_id)
    return render_template('confirmacao.html', presente=presente)

# --- ROTAS API & CHECKOUT ---

@app.route('/api/checkout/<int:item_id>', methods=['POST'])
def checkout(item_id):
    item = Item.query.get_or_404(item_id)
    
    if item.status == 'presenteado' or item.valor_restante <= 0:
        return jsonify({'success': False, 'message': 'Este item já foi 100% presenteado!'}), 400

    data = request.get_json() or {}
    nome_convidado = data.get('nome_convidado', '').strip()
    mensagem = data.get('mensagem', '').strip()

    if not nome_convidado:
        return jsonify({'success': False, 'message': 'Por favor, informe seu nome.'}), 400

    # Processamento do valor da contribuição enviado pelo convidado
    try:
        raw_val = data.get('valor_contribuicao')
        if raw_val is not None and str(raw_val).strip() != '':
            valor_contribuicao = float(raw_val)
        else:
            valor_contribuicao = item.valor_restante
    except (ValueError, TypeError):
        valor_contribuicao = item.valor_restante

    if valor_contribuicao <= 0:
        return jsonify({'success': False, 'message': 'O valor da contribuição deve ser maior que R$ 0,00.'}), 400

    if valor_contribuicao > item.valor_restante:
        valor_contribuicao = item.valor_restante

    valor_contribuicao = round(valor_contribuicao, 2)

    # Cria registro do Presente no status 'pending' com o valor da cota escolhida
    novo_presente = Presente(
        item_id=item.id,
        nome_convidado=nome_convidado,
        mensagem=mensagem,
        valor=valor_contribuicao,
        status_pagamento='pending'
    )
    db.session.add(novo_presente)
    db.session.commit()

    qr_code_base64 = ""
    qr_code_copia_cola = ""
    mp_payment_id = f"LOCAL-PIX-{novo_presente.id}"

    # Tenta usar o SDK do Mercado Pago se o Token estiver disponível
    if mp_sdk:
        try:
            payment_data = {
                "transaction_amount": float(valor_contribuicao),
                "description": f"Contribuição: {item.nome} - Lista do Bebê",
                "payment_method_id": "pix",
                "payer": {
                    "email": f"convidado_{novo_presente.id}@beberegistry.com",
                    "first_name": nome_convidado[:30]
                },
                "notification_url": app.config.get('WEBHOOK_URL')
            }
            payment_response = mp_sdk.payment().create(payment_data)
            res = payment_response.get("response", {})
            
            if "point_of_interaction" in res:
                transaction_data = res["point_of_interaction"]["transaction_data"]
                qr_code_copia_cola = transaction_data.get("qr_code", "")
                qr_code_base64 = transaction_data.get("qr_code_base64", "")
                mp_payment_id = str(res.get("id", mp_payment_id))
        except Exception as e:
            print(f"Erro na integração Mercado Pago SDK: {e}. Alternando para modo de demonstração.")

    # Se o QR code não veio do MP (sem token ou erro/dev mode), gerar dinamicamente
    if not qr_code_copia_cola:
        qr_code_copia_cola = (
            f"00020126580014BR.GOV.BCB.PIX0136bebe-registry-{novo_presente.id}-pix-demo"
            f"520400005303986540{valor_contribuicao:.2f}5802BR5915BEBE REGISTRY6009SAO PAULO62070503***6304ABCD"
        )
        
        img = qrcode.make(qr_code_copia_cola)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        qr_code_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    novo_presente.mp_payment_id = mp_payment_id
    db.session.commit()

    return jsonify({
        'success': True,
        'presente_id': novo_presente.id,
        'item_nome': item.nome,
        'valor_contribuicao': valor_contribuicao,
        'valor_restante': item.valor_restante,
        'total_arrecadado': item.total_arrecadado,
        'porcentagem': item.porcentagem,
        'qr_code_base64': qr_code_base64,
        'qr_code': qr_code_copia_cola
    })

@app.route('/api/simulate-payment/<int:presente_id>', methods=['POST'])
def simulate_payment(presente_id):
    """Rota de auxílio para simulação imediata do pagamento em ambiente de testes/dev."""
    presente = Presente.query.get_or_404(presente_id)
    presente.status_pagamento = 'approved'
    db.session.flush()
    
    # Atualiza o status do item se a arrecadação acumulada atingir a meta
    if presente.item.valor_restante <= 0:
        presente.item.status = 'presenteado'
        
    db.session.commit()

    return jsonify({
        'success': True,
        'redirect_url': url_for('confirmacao', presente_id=presente.id)
    })

@app.route('/api/mural/mensagem', methods=['POST'])
def adicionar_mensagem_avulsa():
    """Rota para adicionar um recado de carinho diretamente pelo FAB no mural."""
    data = request.get_json() or {}
    nome = data.get('nome_convidado', '').strip()
    mensagem = data.get('mensagem', '').strip()

    if not nome or not mensagem:
        return jsonify({'success': False, 'message': 'Nome e mensagem são obrigatórios.'}), 400

    item = Item.query.first()
    if not item:
        return jsonify({'success': False, 'message': 'Nenhum item cadastrado.'}), 400

    novo_recado = Presente(
        item_id=item.id,
        nome_convidado=nome,
        mensagem=mensagem,
        valor=0.0,
        mp_payment_id="AVULSO-FAB",
        status_pagamento="approved"
    )
    db.session.add(novo_recado)
    db.session.commit()

    return jsonify({'success': True})

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook do Mercado Pago para atualização de pagamento."""
    topic = request.args.get('topic') or request.args.get('type')
    payment_id = request.args.get('id') or request.json.get('data', {}).get('id') if request.is_json else None

    if topic == 'payment' and payment_id and mp_sdk:
        try:
            payment_info = mp_sdk.payment().get(payment_id)
            res = payment_info.get("response", {})
            status = res.get("status")

            presente = Presente.query.filter_by(mp_payment_id=str(payment_id)).first()
            if presente:
                presente.status_pagamento = status
                db.session.flush()
                if status == 'approved':
                    if presente.item.valor_restante <= 0:
                        presente.item.status = 'presenteado'
                db.session.commit()
        except Exception as e:
            print(f"Erro ao processar Webhook do Mercado Pago: {e}")

    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
