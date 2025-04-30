from conversor import database
from flask_login import UserMixin
from conversor import login_manager
from datetime import datetime



class User(database.Model, UserMixin):
    __tablename__ = 'user'

    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(150), unique=True, nullable=False)
    nome = database.Column(database.String(150), nullable=False)
    sobrenome = database.Column(database.String(150), nullable=False)
    senha_hash = database.Column(database.String(150), nullable=False)

    suplementos = database.relationship('Suplemento', backref='usuario', lazy=True)
    planejamentos = database.relationship('PlanejamentoItem', backref='usuario', lazy=True)

    def nome_completo(self):
        return f"{self.nome} {self.sobrenome}"


class Suplemento(database.Model):
    __tablename__ = 'suplementos'

    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)

    nome = database.Column(database.String(100), nullable=False)
    tipo = database.Column(database.String(50), nullable=False)
    marca = database.Column(database.String(50))

    carbo = database.Column(database.Float)
    sodio = database.Column(database.Float)
    magnesio = database.Column(database.Float)
    potassio = database.Column(database.Float)
    calcio = database.Column(database.Float)

    cafeina = database.Column(database.Float)
    taurina = database.Column(database.Float)
    beta_alanina = database.Column(database.Float)
    citrulina = database.Column(database.Float)
    creatina = database.Column(database.Float)
    
    coq10 = database.Column(database.Float)
    carnitina = database.Column(database.Float)

    leucina = database.Column(database.Float)
    isoleucina = database.Column(database.Float)
    valina = database.Column(database.Float)
    arginina = database.Column(database.Float)

    vit_b1 = database.Column(database.Float)
    vit_b2 = database.Column(database.Float)
    vit_b3 = database.Column(database.Float)
    vit_b6 = database.Column(database.Float)
    vit_b7 = database.Column(database.Float)
    vit_b9 = database.Column(database.Float)
    vit_b12 = database.Column(database.Float)
    vit_c = database.Column(database.Float)

    def __repr__(self):
        return f'<Suplemento {self.nome}>'


class PlanejamentoItem(database.Model):
    __tablename__ = 'planejamento_itens'

    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    suplemento_id = database.Column(database.Integer, database.ForeignKey('suplementos.id'), nullable=False)
    quantidade = database.Column(database.Integer, nullable=False)

    suplemento = database.relationship('Suplemento', lazy=True)

    def calcular_totais(self):
        def multi(valor):
            return round((valor or 0) * self.quantidade, 2)

        return {
            'carbo': multi(self.suplemento.carbo),
            'sodio': multi(self.suplemento.sodio),
            'magnesio': multi(self.suplemento.magnesio),
            'potassio': multi(self.suplemento.potassio),
            'calcio': multi(self.suplemento.calcio),
            'cafeina': multi(self.suplemento.cafeina),
            'taurina': multi(self.suplemento.taurina),
            'beta_alanina': multi(self.suplemento.beta_alanina),
            'citrulina': multi(self.suplemento.citrulina),
            'creatina': multi(self.suplemento.creatina),
            'coq10': multi(self.suplemento.coq10),
            'carnitina': multi(self.suplemento.carnitina),
            'leucina': multi(self.suplemento.leucina),
            'isoleucina': multi(self.suplemento.isoleucina),
            'valina': multi(self.suplemento.valina),
            'arginina': multi(self.suplemento.arginina),
            'vit_b1': multi(self.suplemento.vit_b1),
            'vit_b2': multi(self.suplemento.vit_b2),
            'vit_b3': multi(self.suplemento.vit_b3),
            'vit_b6': multi(self.suplemento.vit_b6),
            'vit_b7': multi(self.suplemento.vit_b7),
            'vit_b9': multi(self.suplemento.vit_b9),
            'vit_b12': multi(self.suplemento.vit_b12),
            'vit_c': multi(self.suplemento.vit_c),
        }

    def __repr__(self):
        return f'<PlanejamentoItem {self.suplemento.nome} x {self.quantidade}>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class ResumoSalvo(database.Model):
    __tablename__ = 'resumos_salvos'

    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    nome_treino = database.Column(database.String(100), nullable=False)
    data = database.Column(database.Date, nullable=False)
    comentario = database.Column(database.Text)
    resumo_dados = database.Column(database.JSON, nullable=False)
    tempo_natacao = database.Column(database.Float)
    tempo_bike = database.Column(database.Float)
    tempo_corrida = database.Column(database.Float)
    tempo_total = database.Column(database.Float)
    criado_em = database.Column(database.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ResumoSalvo {self.nome_treino} - {self.data}>'
    
    
    