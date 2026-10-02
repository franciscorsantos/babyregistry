from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    imagem_url = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='disponivel') # 'disponivel', 'presenteado'
    destaque = db.Column(db.Boolean, default=False) # Para badge "Must Have"

    presentes = db.relationship('Presente', backref='item', lazy=True, cascade='all, delete-orphan')

    @property
    def total_arrecadado(self):
        total = db.session.query(db.func.sum(Presente.valor)).filter(
            Presente.item_id == self.id,
            Presente.status_pagamento == 'approved'
        ).scalar()
        return round(total or 0.0, 2)

    @property
    def valor_restante(self):
        restante = self.valor - self.total_arrecadado
        return max(0.0, round(restante, 2))

    @property
    def porcentagem(self):
        if not self.valor or self.valor <= 0:
            return 100
        pct = (self.total_arrecadado / self.valor) * 100
        return min(100, int(round(pct)))

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'categoria': self.categoria,
            'valor': self.valor,
            'total_arrecadado': self.total_arrecadado,
            'valor_restante': self.valor_restante,
            'porcentagem': self.porcentagem,
            'imagem_url': self.imagem_url,
            'status': self.status,
            'destaque': self.destaque
        }

class Presente(db.Model):
    __tablename__ = 'presentes'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    nome_convidado = db.Column(db.String(120), nullable=False)
    mensagem = db.Column(db.Text, nullable=True)
    valor = db.Column(db.Float, nullable=False, default=0.0)
    mp_payment_id = db.Column(db.String(100), nullable=True)
    status_pagamento = db.Column(db.String(20), nullable=False, default='pending') # 'pending', 'approved', 'cancelled'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'item_nome': self.item.nome if self.item else '',
            'nome_convidado': self.nome_convidado,
            'mensagem': self.mensagem,
            'valor': self.valor,
            'mp_payment_id': self.mp_payment_id,
            'status_pagamento': self.status_pagamento,
            'created_at': self.created_at.strftime('%d/%m/%Y %H:%M') if self.created_at else ''
        }
