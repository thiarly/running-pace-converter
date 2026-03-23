from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField, IntegerField, PasswordField, ValidationError, TextAreaField, DateField, DecimalField
from wtforms.validators import DataRequired, Optional, NumberRange, InputRequired, Email, Length, EqualTo
from decimal import Decimal, InvalidOperation
from conversor.models import User


class FloatFieldBR(FloatField):
    def process_formdata(self, valuelist):
        if valuelist:
            valor = valuelist[0]

            if valor is None or valor.strip() == "":
                self.data = None
                return

            valor = valor.replace(",", ".").strip()

            try:
                self.data = float(valor)
            except ValueError:
                self.data = None
                raise ValueError("Número inválido. Use 2,5 ou 2.5")


class DecimalFieldBR(DecimalField):
    def process_formdata(self, valuelist):
        if valuelist:
            valor = valuelist[0]

            if valor is None or valor.strip() == "":
                self.data = None
                return

            valor = valor.replace(",", ".").strip()

            try:
                self.data = Decimal(valor)
            except (InvalidOperation, ValueError):
                self.data = None
                raise ValueError("Número inválido. Use 2,5 ou 2.5")


class SuplementoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    tipo = SelectField('Tipo', choices=[('Gel', 'Gel'), ('Carboidrato', 'Carboidrato'), ('Garrafa', 'Garrafa'), ('Proteina', 'Proteína'), ('Eletrólitos', 'Eletrólitos'), ('Pré Treino', 'Pré Treino')], validators=[DataRequired()])
    marca = StringField('Marca', validators=[Optional()])
    
    gramas_por_porcao = FloatFieldBR('Gramas por Porção', validators=[DataRequired(), NumberRange(min=0.01)])
    descricao_porcao = StringField('Descrição da Porção', validators=[Optional()])

    carbo = FloatFieldBR('Carboidrato (g)', validators=[Optional()])
    sodio = FloatFieldBR('Sódio (mg)', validators=[Optional()])
    magnesio = FloatFieldBR('Magnésio (mg)', validators=[Optional()])
    potassio = FloatFieldBR('Potássio (mg)', validators=[Optional()])
    cloro = FloatFieldBR('Cloro (mg)', validators=[Optional()])
    fosforo = FloatFieldBR('Fósforo (mg)', validators=[Optional()])
    zinco = FloatFieldBR('Zinco (mg)', validators=[Optional()])
    calcio = FloatFieldBR('Cálcio (mg)', validators=[Optional()])

    cafeina = FloatFieldBR('Cafeína (mg)', validators=[Optional()])
    taurina = FloatFieldBR('Taurina (mg)', validators=[Optional()])
    beta_alanina = FloatFieldBR('Beta-Alanina (mg)', validators=[Optional()])
    citrulina = FloatFieldBR('Citrulina (mg)', validators=[Optional()])
    creatina = FloatFieldBR('Creatina (mg)', validators=[Optional()])

    coq10 = FloatFieldBR('Coenzima Q10 (mg)', validators=[Optional()])
    carnitina = FloatFieldBR('L-Carnitina (mg)', validators=[Optional()])

    leucina = FloatFieldBR('Leucina (mg)', validators=[Optional()])
    isoleucina = FloatFieldBR('Isoleucina (mg)', validators=[Optional()])
    valina = FloatFieldBR('Valina (mg)', validators=[Optional()])
    arginina = FloatFieldBR('Arginina (mg)', validators=[Optional()])
    niacina = FloatFieldBR('Niacina (mg)', validators=[Optional()])

    vit_b1 = FloatFieldBR('Vitamina B1 (mg)', validators=[Optional()])
    vit_b2 = FloatFieldBR('Vitamina B2 (mg)', validators=[Optional()])
    vit_b3 = FloatFieldBR('Vitamina B3 (mg)', validators=[Optional()])
    vit_b5 = FloatFieldBR('Vitamina B5 (mg)', validators=[Optional()])
    vit_b6 = FloatFieldBR('Vitamina B6 (mg)', validators=[Optional()])
    vit_b7 = FloatFieldBR('Vitamina B7 (µg)', validators=[Optional()])
    vit_b9 = FloatFieldBR('Vitamina B9 (µg)', validators=[Optional()])
    vit_b12 = FloatFieldBR('Vitamina B12 (µg)', validators=[Optional()])
    vit_c = FloatFieldBR('Vitamina C (mg)', validators=[Optional()])
    vit_e = FloatFieldBR('Vitamina E (mg)', validators=[Optional()])
    vit_ferro = FloatFieldBR('Ferro (mg)', validators=[Optional()])
    
    comentario = TextAreaField('Comentário', render_kw={"placeholder": "Anotações, misturas, fabricante..."})
    ingredientes = TextAreaField('Ingredientes', render_kw={"placeholder": "Composição ou ingredientes usados..."})

    submit = SubmitField('Salvar')


class PlanningItemForm(FlaskForm):
    suplemento_id = SelectField('Produto', coerce=int, validators=[DataRequired()])
    quantidade = DecimalFieldBR('Quantidade', places=2, rounding=None, validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Adicionar')
    
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(), Length(max=150)])
    senha = PasswordField('Senha', validators=[InputRequired()])
    submit = SubmitField('Entrar')
    

class RegisterForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(message="O nome é obrigatório.")])
    sobrenome = StringField('Sobrenome', validators=[DataRequired(message="O sobrenome é obrigatório.")])
    email = StringField('Email', validators=[
        DataRequired(message="O e-mail é obrigatório."),
        Email(message="Informe um e-mail válido.")
    ])
    senha = PasswordField('Senha', validators=[
        DataRequired(message="A senha é obrigatória."),
        Length(min=6, message="A senha deve ter no mínimo 6 caracteres.")
    ])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[
        DataRequired(message="Confirme a senha."),
        EqualTo('senha', message="As senhas devem ser iguais.")
    ])
    submit = SubmitField('Cadastrar')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Este e-mail já está cadastrado.")
        

class SalvarResumoForm(FlaskForm):
    nome_treino = StringField('Nome do Treino', validators=[DataRequired()])
    data = DateField("Data", format="%Y-%m-%d", validators=[DataRequired()])
    comentario = TextAreaField('Comentário')
    submit = SubmitField('Salvar Resumo')

        
class ResumoForm(FlaskForm):
    tempo_natacao_horas = IntegerField('Horas Natação', validators=[Optional(), NumberRange(min=0)])
    tempo_bike_horas = IntegerField('Horas Bike', validators=[Optional(), NumberRange(min=0)])
    tempo_corrida_horas = IntegerField('Horas Corrida', validators=[Optional(), NumberRange(min=0)])
    tempo_natacao_minutos = IntegerField('Minutos Natação', validators=[Optional(), NumberRange(min=0, max=59)])
    tempo_bike_minutos = IntegerField('Minutos Bike', validators=[Optional(), NumberRange(min=0, max=59)])
    tempo_corrida_minutos = IntegerField('Minutos Corrida', validators=[Optional(), NumberRange(min=0, max=59)])

    submit_calcular = SubmitField('Calcular Resumo')
    submit_limpar = SubmitField('Limpar Tela')
    submit_salvar = SubmitField('Salvar Resumo')