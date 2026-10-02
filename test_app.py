from app import app, db
from models import Item, Presente
from seed import seed_database

def test_application_flow():
    client = app.test_client()

    with app.app_context():
        # Limpar banco de teste para ter estado consistente
        db.drop_all()
        db.create_all()
        seed_database()

        print("--- 1. Testando Rota Principal (Vitrine /) ---")
        res = client.get('/')
        assert res.status_code == 200, f"Erro na rota /: {res.status_code}"
        assert b"Beb" in res.data, "Nome Bebê Registry não encontrado no HTML"
        print("[OK] Rota principal (/) funcionando!")

        print("\n--- 2. Testando Rota do Mural de Recados (/mural) ---")
        res = client.get('/mural')
        assert res.status_code == 200, f"Erro na rota /mural: {res.status_code}"
        print("[OK] Rota /mural funcionando!")

        print("\n--- 3. Testando API de Checkout com Contribuição Parcial (Vaquinha) ---")
        item_disponivel = Item.query.filter_by(status='disponivel').first()
        assert item_disponivel is not None, "Nenhum item disponível encontrado no banco"
        
        # Testar primeira contribuição parcial de 50%
        cota_1 = round(item_disponivel.valor_restante / 2, 2)
        checkout_payload_1 = {
            "nome_convidado": "Tia Claudia Teste",
            "mensagem": "Primeira cota para ajudar os papais!",
            "valor_contribuicao": cota_1
        }
        res = client.post(f'/api/checkout/{item_disponivel.id}', json=checkout_payload_1)
        assert res.status_code == 200, f"Erro na API de checkout cota 1: {res.status_code}"
        data1 = res.get_json()
        assert data1['success'] is True
        assert data1['valor_contribuicao'] == cota_1
        presente_id_1 = data1['presente_id']

        # Simular aprovação do primeiro pagamento
        res = client.post(f'/api/simulate-payment/{presente_id_1}')
        assert res.status_code == 200
        
        db.session.expire_all()
        item_disponivel = db.session.get(Item, item_disponivel.id)
        assert item_disponivel.total_arrecadado == cota_1
        assert item_disponivel.status == 'disponivel', "Item com arrecadação parcial não deve mudar para 'presenteado'"
        print(f"[OK] Cota 1 de R$ {cota_1} aprovada! Progresso: {item_disponivel.porcentagem}% (Restam R$ {item_disponivel.valor_restante})")

        # Testar segunda contribuição completando os 100%
        cota_2 = item_disponivel.valor_restante
        checkout_payload_2 = {
            "nome_convidado": "Tio Marcos Teste",
            "mensagem": "Completando o valor restante do presente!",
            "valor_contribuicao": cota_2
        }
        res = client.post(f'/api/checkout/{item_disponivel.id}', json=checkout_payload_2)
        assert res.status_code == 200
        data2 = res.get_json()
        presente_id_2 = data2['presente_id']

        # Simular aprovação do segundo pagamento
        res = client.post(f'/api/simulate-payment/{presente_id_2}')
        assert res.status_code == 200

        db.session.expire_all()
        item_disponivel = db.session.get(Item, item_disponivel.id)
        assert item_disponivel.status == 'presenteado', "Status do item não mudou para 'presenteado' após atingir 100%"
        assert item_disponivel.porcentagem == 100
        print("[OK] Cota 2 aprovada! Item atingiu 100% e atualizou status para 'presenteado'!")

        print("\n--- 4. Testando Rota de Confirmação (/confirmacao/<id>) ---")
        res = client.get(f'/confirmacao/{presente_id_1}')
        assert res.status_code == 200, f"Erro na rota /confirmacao: {res.status_code}"
        assert b"Tia Claudia Teste" in res.data, "Nome do convidado não encontrado no recibo"
        print("[OK] Tela de confirmação/recibo gerada perfeitamente!")

        print("\n--- 5. Testando Envio de Recado Avulso no Mural (/api/mural/mensagem) ---")
        res = client.post('/api/mural/mensagem', json={
            "nome_convidado": "Vovo Ana",
            "mensagem": "Com todo o carinho do mundo para o meu netinho querido!"
        })
        assert res.status_code == 200, f"Erro ao adicionar recado avulso: {res.status_code}"
        print("[OK] Recado avulso adicionado com sucesso!")

        print("\nSUCESSO: TODOS OS TESTES DA VAQUINHA / COTAS PASSARAM COM SUCESSO ABSOLUTO!")

if __name__ == "__main__":
    test_application_flow()
