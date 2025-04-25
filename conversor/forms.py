from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Optional, NumberRange


class SuplementoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    tipo = SelectField('Tipo', choices=[('Gel', 'Gel'), ('Garrafa', 'Garrafa'), ('Eletrólitos', 'Eletrólitos'), ('Pré Treino', 'Pré Treino')], validators=[DataRequired()])
    marca = StringField('Marca', validators=[Optional()])

    carbo = FloatField('Carboidrato (g)', validators=[Optional()])
    sodio = FloatField('Sódio (mg)', validators=[Optional()])
    magnesio = FloatField('Magnésio (mg)', validators=[Optional()])
    potassio = FloatField('Potássio (mg)', validators=[Optional()])
    calcio = FloatField('Cálcio (mg)', validators=[Optional()])

    cafeina = FloatField('Cafeína (mg)', validators=[Optional()])
    taurina = FloatField('Taurina (mg)', validators=[Optional()])
    beta_alanina = FloatField('Beta-Alanina (mg)', validators=[Optional()])
    citrulina = FloatField('Citrulina (mg)', validators=[Optional()])
    creatina = FloatField('Creatina (mg)', validators=[Optional()])

    coq10 = FloatField('Coenzima Q10 (mg)', validators=[Optional()])
    carnitina = FloatField('L-Carnitina (mg)', validators=[Optional()])

    leucina = FloatField('Leucina (mg)', validators=[Optional()])
    isoleucina = FloatField('Isoleucina (mg)', validators=[Optional()])
    valina = FloatField('Valina (mg)', validators=[Optional()])
    arginina = FloatField('Arginina (mg)', validators=[Optional()])

    vit_b1 = FloatField('Vitamina B1 (mg)', validators=[Optional()])
    vit_b2 = FloatField('Vitamina B2 (mg)', validators=[Optional()])
    vit_b3 = FloatField('Vitamina B3 (mg)', validators=[Optional()])
    vit_b6 = FloatField('Vitamina B6 (mg)', validators=[Optional()])
    vit_b7 = FloatField('Vitamina B7 (µg)', validators=[Optional()])
    vit_b9 = FloatField('Vitamina B9 (µg)', validators=[Optional()])
    vit_b12 = FloatField('Vitamina B12 (µg)', validators=[Optional()])
    vit_c = FloatField('Vitamina C (mg)', validators=[Optional()])

    submit = SubmitField('Salvar')



class PlanningItemForm(FlaskForm):
    suplemento_id = SelectField('Produto', coerce=int, validators=[DataRequired()])
    quantidade = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Adicionar')