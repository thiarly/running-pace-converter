from conversor import database


class Suplemento(database.Model):
    __tablename__ = 'suplementos'

    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(100), nullable=False)
    tipo = database.Column(database.String(50), nullable=False)  # ex: Gel, Garrafa, Cápsula
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
