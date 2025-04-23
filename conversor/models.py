from conversor import db


class Suplemento(db.Model):
    __tablename__ = 'suplementos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # ex: Gel, Garrafa, Cápsula
    marca = db.Column(db.String(50))

    carbo = db.Column(db.Float)
    sodio = db.Column(db.Float)
    magnesio = db.Column(db.Float)
    potassio = db.Column(db.Float)
    calcio = db.Column(db.Float)

    cafeina = db.Column(db.Float)
    taurina = db.Column(db.Float)
    beta_alanina = db.Column(db.Float)
    citrulina = db.Column(db.Float)
    creatina = db.Column(db.Float)
    
    
    coq10 = db.Column(db.Float)
    carnitina = db.Column(db.Float)

    leucina = db.Column(db.Float)
    isoleucina = db.Column(db.Float)
    valina = db.Column(db.Float)
    arginina = db.Column(db.Float)

    vit_b1 = db.Column(db.Float)
    vit_b2 = db.Column(db.Float)
    vit_b3 = db.Column(db.Float)
    vit_b6 = db.Column(db.Float)
    vit_b7 = db.Column(db.Float)
    vit_b9 = db.Column(db.Float)
    vit_b12 = db.Column(db.Float)
    vit_c = db.Column(db.Float)

    def __repr__(self):
        return f'<Suplemento {self.nome}>'
