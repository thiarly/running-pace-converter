from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField, IntegerField, PasswordField, ValidationError, TextAreaField, DateField
from wtforms.validators import DataRequired, Optional, NumberRange, InputRequired, Email, Length, EqualTo
from conversor.models import User



class SuplementoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    tipo = SelectField('Tipo', choices=[('Gel', 'Gel'), ('Carboidrato', 'Carboidrato'), ('Garrafa', 'Garrafa'), ('Proteina', 'Proteína'), ('Eletrólitos', 'Eletrólitos'), ('Pré Treino', 'Pré Treino')], validators=[DataRequired()])
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
    
    comentario = TextAreaField('Comentário', render_kw={"placeholder": "Anotações, misturas, fabricante..."})
    ingredientes = TextAreaField('Ingredientes', render_kw={"placeholder": "Composição ou ingredientes usados..."})

    submit = SubmitField('Salvar')



class PlanningItemForm(FlaskForm):
    suplemento_id = SelectField('Produto', coerce=int, validators=[DataRequired()])
    quantidade = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Adicionar')
    
    
class ResumoForm(FlaskForm):
    tempo_natacao_horas = IntegerField('Horas Natação', validators=[Optional()])
    tempo_natacao_minutos = IntegerField('Minutos Natação', validators=[Optional()])

    tempo_bike_horas = IntegerField('Horas Bike', validators=[Optional()])
    tempo_bike_minutos = IntegerField('Minutos Bike', validators=[Optional()])

    tempo_corrida_horas = IntegerField('Horas Corrida', validators=[Optional()])
    tempo_corrida_minutos = IntegerField('Minutos Corrida', validators=[Optional()])

    submit = SubmitField('Calcular Resumo')
    limpar = SubmitField('Limpar Tela')



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
    submit_salvar = SubmitField('Salvar Resumo')  # se já quiser prever esse botão


