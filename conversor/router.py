from flask import Flask, render_template, request, redirect, url_for, flash, session
from conversor import app, database

from conversor.forms import SuplementoForm, PlanningItemForm, ResumoForm, LoginForm, RegisterForm, ResumoForm, SalvarResumoForm
from conversor.models import Suplemento, PlanejamentoItem, User, ResumoSalvo

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, logout_user

import json
from datetime import date




from conversor.utils import (
    convert_pace, calc_average_speed_bike,
    calc_swim_pace, calculate_estimated_time,
    calculate_estimated_distance, convert_pace_to_speed,
    convert_speed_to_pace, convert_milha_pace,
    convert_pace_milha, convert_km_to_miles,
    convert_miles_to_km, calculate_vo2max,
    race_predictions, calculate_pace_km, calculate_paces_by_vo2max,
    race_predictions_from_3k, agrupar_por_categoria
)





@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.senha_hash, form.senha.data):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('listar_suplementos'))
        else:
            flash('Email ou senha inválidos.', 'danger')
    return render_template('login.html', form=form)


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.senha.data)
        novo_usuario = User(
            nome=form.nome.data,
            sobrenome=form.sobrenome.data,
            email=form.email.data,
            senha_hash=hashed_password
        )
        database.session.add(novo_usuario)
        database.session.commit()
        flash('Cadastro realizado! Faça login.', 'success')
        return redirect(url_for('login'))
    return render_template('cadastro.html', form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso.', 'success')
    return redirect(url_for('login'))
 



@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        hour = request.form.get('hour')
        minute = request.form.get('minute')
        second = request.form.get('second')
        distance = request.form.get('distance')
        activity = request.form.get('activity')

        if not hour or not minute or not second or not distance:
            return render_template('home.html', error='Por favor, forneça valores para a hora, minuto, segundo e distância.')

        hour = int(hour)
        minute = int(minute)
        second = int(second)
        distance = float(distance)

        time = hour * 3600 + minute * 60 + second  # Converter o tempo total em segundos

        if activity == 'corrida':
            pace_km, pace_mile = convert_pace(time, distance)
            return render_template('home.html', pace_km=pace_km, pace_mile=pace_mile)
        
        elif activity == 'ciclismo':
            avg_speed = calc_average_speed_bike(time, distance)
            return render_template('home.html', avg_speed=avg_speed)

        elif activity == 'natacao':
            pace_100m = calc_swim_pace(time, distance)
            return render_template('home.html', pace_100m=pace_100m)

        else:
            return render_template('home.html', error='Por favor, selecione uma atividade.')
            
    return render_template('home.html')



@app.route('/estimativa-tempo', methods=['GET', 'POST'])
def estimativa_tempo():
    if request.method == 'POST':
        distance = request.form.get('distance')
        pace = request.form.get('pace')

        if not distance or not pace:
            return render_template('estimativa_tempo.html', error='Por favor, forneça valores para a distância e o pace.')

        distance = float(distance)
        estimated_time = calculate_estimated_time(distance, pace)
        
        return render_template('estimativa_tempo.html', estimated_time=estimated_time)

    return render_template('estimativa_tempo.html')


@app.route('/estimativa_distancia', methods=['GET', 'POST'])
def estimativa_distancia():
    if request.method == 'POST':
        hour = request.form.get('hour')
        minute = request.form.get('minute')
        second = request.form.get('second')
        pace = request.form.get('pace')

        if not hour or not minute or not second or not pace:
            return render_template('estimativa_distancia.html', error='Por favor, forneça valores para a hora, minuto, segundo e o pace.')

        hour = int(hour)
        minute = int(minute)
        second = int(second)
        time = hour * 3600 + minute * 60 + second  # Converter o tempo total em segundos

        estimated_distance = calculate_estimated_distance(time, pace)
        
        return render_template('estimativa_distancia.html', estimated_distance=estimated_distance)

    return render_template('estimativa_distancia.html')


@app.route('/conversao_pace', methods=['GET', 'POST'])
def conversao_pace():
    if request.method == 'POST':
        pace = request.form.get('pace')

        if not pace:
            return render_template('conversao_pace.html', error='Por favor, forneça um valor para o pace.')

        speed_kmh = convert_pace_to_speed(pace)
        
        return render_template('conversao_pace.html', speed_kmh=speed_kmh)

    return render_template('conversao_pace.html')


@app.route('/conversao_velocidade', methods=['GET', 'POST'])
def conversao_velocidade():
    if request.method == 'POST':
        speed_kmh = request.form.get('speed_kmh')

        if not speed_kmh:
            return render_template('conversao_velocidade.html', error='Por favor, forneça um valor para a velocidade.')

        speed_kmh = float(speed_kmh)
        pace = convert_speed_to_pace(speed_kmh)
        
        return render_template('conversao_velocidade.html', pace=pace)

    return render_template('conversao_velocidade.html')



@app.route('/conversao_milha_pace', methods=['GET', 'POST'])
def conversao_milha_pace():
    if request.method == 'POST':
        pace_km = request.form.get('pace_km')

        if not pace_km:
            return render_template('conversao_milha_pace.html', error='Por favor, forneça um valor para o pace em km.')

        pace_mile = convert_milha_pace(pace_km)
        
        return render_template('conversao_milha_pace.html', pace_mile=pace_mile)

    return render_template('conversao_milha_pace.html')




@app.route('/conversao_pace_milha', methods=['GET', 'POST'])
def conversao_pace_milha():
    if request.method == 'POST':
        pace_km = request.form.get('pace_km')

        if not pace_km:
            return render_template('conversao_pace_milha.html', error='Por favor, forneça um valor para o pace em km.')

        pace_mile = convert_pace_milha(pace_km)
        
        return render_template('conversao_pace_milha.html', pace_mile=pace_mile)

    return render_template('conversao_pace_milha.html')



@app.route('/tabela_pace')
def tabela_pace():
    pace_table = []
    for speed_kmh in [x * 0.5 for x in range(16, 47)]:  # De 8 km/h a 23 km/h com intervalo de 0,5 km/h
        pace_km = convert_speed_to_pace(speed_kmh)
        pace_mile = convert_pace_milha(pace_km)
        pace_table.append({
            "speed_kmh": speed_kmh,
            "pace_km": pace_km,
            "pace_mile": pace_mile
        })
    return render_template('tabela_pace.html', pace_table=pace_table)


@app.route('/conversao_km_para_milhas', methods=['GET', 'POST'])
def conversao_km_para_milhas():
    if request.method == 'POST':
        km = request.form.get('km')

        if not km:
            return render_template('conversao_km_para_milhas.html', error='Por favor, forneça uma distância em quilômetros.')

        km = float(km)
        miles = convert_km_to_miles(km)
        
        return render_template('conversao_km_para_milhas.html', miles=miles)

    return render_template('conversao_km_para_milhas.html')


@app.route('/conversao_milhas_para_km', methods=['GET', 'POST'])
def conversao_milhas_para_km():
    if request.method == 'POST':
        miles = request.form.get('miles')

        if not miles:
            return render_template('conversao_milhas_para_km.html', error='Por favor, forneça uma distância em milhas.')

        miles = float(miles)
        km = convert_miles_to_km(miles)
        
        return render_template('conversao_milhas_para_km.html', km=km)

    return render_template('conversao_milhas_para_km.html')


@app.route('/calculadora_vo2max', methods=['GET', 'POST'])
def calculadora_vo2max():
    if request.method == 'POST':
        time = request.form.get('time')

        if not time:
            return render_template('calculadora_vo2max.html', error='Por favor, forneça um tempo válido.')

        hours, minutes, seconds = map(int, time.split(':'))
        time_seconds = hours * 3600 + minutes * 60 + seconds

        pace_seconds_per_km = time_seconds / 10  # Distância de 10 km
        pace_km = calculate_pace_km(time_seconds, 10)
        vo2max = calculate_vo2max(time_seconds, 10)
        paces = calculate_paces_by_vo2max(pace_seconds_per_km)
        predictions = race_predictions(time_seconds, 10)
        
        return render_template('calculadora_vo2max.html', vo2max=vo2max, paces=paces, predictions=predictions, pace_km=pace_km)

    return render_template('calculadora_vo2max.html')


@app.route('/previsao_prova_3k', methods=['GET', 'POST'])
def previsao_prova_3k():
    if request.method == 'POST':
        time = request.form.get('time')

        if not time:
            return render_template('previsao_prova_3k.html', error='Por favor, forneça um tempo válido.')

        minutes, seconds = map(int, time.split(':'))
        time_seconds = minutes * 60 + seconds

        predictions = race_predictions_from_3k(time_seconds, 3)
        pace_km = calculate_pace_km(time_seconds, 3)
        
        return render_template('previsao_prova_3k.html', predictions=predictions, pace_km=pace_km)

    return render_template('previsao_prova_3k.html')


@app.route('/zonas')
def zonas():
    return render_template('zonas.html')


import os

@app.route('/sobre')
def sobre():
    image_directory = os.path.join(app.root_path, 'static/image')
    images = [os.path.join('image', image) for image in os.listdir(image_directory) if image.endswith('.jpg')]
    return render_template('sobre.html', images=images)



# Cadastro de suplemento
@app.route('/suplementos/novo', methods=['GET', 'POST'])
@login_required
def novo_suplemento():
    form = SuplementoForm()
    
    if form.validate_on_submit():
        suplemento = Suplemento(
            nome=form.nome.data,
            tipo=form.tipo.data,
            marca=form.marca.data,
            carbo=form.carbo.data,
            sodio=form.sodio.data,
            magnesio=form.magnesio.data,
            potassio=form.potassio.data,
            calcio=form.calcio.data,
            cafeina=form.cafeina.data,
            taurina=form.taurina.data,
            beta_alanina=form.beta_alanina.data,
            citrulina=form.citrulina.data,
            creatina=form.creatina.data,
            coq10=form.coq10.data,
            carnitina=form.carnitina.data,
            leucina=form.leucina.data,
            isoleucina=form.isoleucina.data,
            valina=form.valina.data,
            arginina=form.arginina.data,
            vit_b1=form.vit_b1.data,
            vit_b2=form.vit_b2.data,
            vit_b3=form.vit_b3.data,
            vit_b6=form.vit_b6.data,
            vit_b7=form.vit_b7.data,
            vit_b9=form.vit_b9.data,
            vit_b12=form.vit_b12.data,
            vit_c=form.vit_c.data,
            user_id=current_user.id  # 👈 liga ao usuário
        )
        database.session.add(suplemento)
        database.session.commit()
        flash('Suplemento cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_suplementos'))
    return render_template('cadastro_suplemento.html', form=form)




# Lista de suplementos
@app.route('/suplementos')
@login_required
def listar_suplementos():
    filtro = request.args.get('filtro', '')
    ordenar = request.args.get('ordenar', '')
    direcao = request.args.get('direcao', 'desc')

    query = Suplemento.query.filter_by(user_id=current_user.id)  # 👈 só do usuário logado

    if filtro:
        query = query.filter(
            Suplemento.nome.ilike(f'%{filtro}%') | Suplemento.tipo.ilike(f'%{filtro}%')
        )

    if ordenar == 'carbo':
        query = query.order_by(Suplemento.carbo.asc() if direcao == 'asc' else Suplemento.carbo.desc())
    elif ordenar == 'sodio':
        query = query.order_by(Suplemento.sodio.asc() if direcao == 'asc' else Suplemento.sodio.desc())

    suplementos = query.all()
    return render_template(
        'listar_suplementos.html',
        suplementos=suplementos,
        filtro=filtro,
        ordenar=ordenar,
        direcao=direcao
    )

# Excluir suplemento
@app.route('/suplementos/excluir/<int:id>', methods=['GET'])
@login_required
def excluir_suplemento(id):
    suplemento = Suplemento.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    database.session.delete(suplemento)
    database.session.commit()
    flash('Suplemento excluído com sucesso!', 'success')
    return redirect(url_for('listar_suplementos'))


# Editar suplemento
@app.route('/suplementos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_suplemento(id):
    suplemento = Suplemento.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = SuplementoForm(obj=suplemento)

    if form.validate_on_submit():
        form.populate_obj(suplemento)
        database.session.commit()
        flash('Suplemento editado com sucesso!', 'success')
        return redirect(url_for('listar_suplementos'))

    return render_template('editar_suplemento.html', form=form, suplemento=suplemento)

# Planejamento
@app.route('/planejamento', methods=['GET', 'POST'])
@login_required
def planejamento():
    form = PlanningItemForm()
    form.suplemento_id.choices = [(s.id, s.nome) for s in Suplemento.query.filter_by(user_id=current_user.id)]

    if form.validate_on_submit():
        item_existente = PlanejamentoItem.query.filter_by(
            suplemento_id=form.suplemento_id.data, user_id=current_user.id
        ).first()
        if item_existente:
            item_existente.quantidade += form.quantidade.data
        else:
            novo_item = PlanejamentoItem(
                suplemento_id=form.suplemento_id.data,
                quantidade=form.quantidade.data,
                user_id=current_user.id
            )
            database.session.add(novo_item)

        database.session.commit()
        flash('Item adicionado/atualizado com sucesso!', 'success')
        return redirect(url_for('planejamento'))

    itens = PlanejamentoItem.query.filter_by(user_id=current_user.id).all()
    totais = calcular_totais_planejamento(itens)

    return render_template('planejamento.html', form=form, itens=itens, totais=totais)


# Atualizar quantidade no planejamento
@app.route('/planejamento/atualizar/<int:item_id>', methods=['POST'])
@login_required
def atualizar_quantidade(item_id):
    item = PlanejamentoItem.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
    nova_quantidade = request.form.get('quantidade', type=int)
    if nova_quantidade and nova_quantidade > 0:
        item.quantidade = nova_quantidade
        database.session.commit()
        flash('Quantidade atualizada com sucesso!', 'success')
    else:
        flash('Quantidade inválida.', 'danger')
    return redirect(url_for('planejamento'))


# Remover item do planejamento
@app.route('/planejamento/remover/<int:item_id>', methods=['POST'])
@login_required
def remover_item(item_id):
    item = PlanejamentoItem.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
    database.session.delete(item)
    database.session.commit()
    flash('Item removido do planejamento.', 'success')
    return redirect(url_for('planejamento'))


# Cálculo de totais do planejamento
def calcular_totais_planejamento(itens):
    totais = {
        'carbo': 0, 'sodio': 0, 'magnesio': 0, 'potassio': 0, 'calcio': 0,
        'cafeina': 0, 'taurina': 0, 'beta_alanina': 0, 'citrulina': 0,
        'creatina': 0, 'coq10': 0, 'carnitina': 0,
        'leucina': 0, 'isoleucina': 0, 'valina': 0, 'arginina': 0,                           
        'vit_b1': 0, 'vit_b2': 0, 'vit_b3': 0, 'vit_b6': 0,
        'vit_b7': 0, 'vit_b9': 0, 'vit_b12': 0, 'vit_c': 0
    }
    
    for item in itens:
        suplemento = item.suplemento
        for key in totais:
            valor = getattr(suplemento, key) or 0
            totais[key] += valor * item.quantidade

    return totais


# Resumo
@app.route('/resumo', methods=['GET', 'POST'])
@login_required
def resumo_view():
    form = ResumoForm()

    if request.method == 'POST' and 'limpar' in request.form:
        return redirect(url_for('resumo_view'))

    itens = PlanejamentoItem.query.filter_by(user_id=current_user.id).all()
    totais = calcular_totais_planejamento(itens)

    totais_por_hora = {}
    tempo_total = 0
    resumo_dados = {}

    if form.validate_on_submit():
        tempo_natacao = (form.tempo_natacao_horas.data or 0) + (form.tempo_natacao_minutos.data or 0) / 60
        tempo_bike = (form.tempo_bike_horas.data or 0) + (form.tempo_bike_minutos.data or 0) / 60
        tempo_corrida = (form.tempo_corrida_horas.data or 0) + (form.tempo_corrida_minutos.data or 0) / 60

        tempo_total = tempo_natacao + tempo_bike + tempo_corrida

        if tempo_total > 0:
            for key, valor in totais.items():
                totais_por_hora[key] = round(valor / tempo_total, 2)
            resumo_dados = agrupar_por_categoria(totais_por_hora)

        session['resumo_dados'] = json.dumps(resumo_dados)
        flash("Resumo calculado com sucesso!", "success")

    # 🔽 Adicione isso aqui
    resumos = ResumoSalvo.query.filter_by(user_id=current_user.id).order_by(ResumoSalvo.data.desc()).all()
    print("Tipo de resumo:", type(resumo_dados), resumo_dados)

    return render_template(
        "resumo.html",
        form=form,
        totais=totais_por_hora,
        resumo=resumo_dados,
        tempo_total=round(tempo_total, 2),
        current_date=date.today().isoformat(),
        resumos=resumos  # <-- novo contexto
    )
            
    
@app.route('/salvar_resumo', methods=['GET', 'POST'])
@login_required
def salvar_resumo():
    form = SalvarResumoForm()

    def parse_float(value):
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    if form.validate_on_submit():
        print("Formulário validado")
    else:
        print("Formulário NÃO validado")
        print(form.errors)

    resumo_json = session.get('resumo_dados')
    if not resumo_json:
        flash("Nenhum resumo disponível para salvar. Por favor, calcule um resumo antes.", "danger")
        return redirect(url_for('resumo_view'))

    if form.validate_on_submit():
        tempo_natacao = parse_float(request.form.get("tempo_natacao_horas")) + parse_float(request.form.get("tempo_natacao_minutos")) / 60
        tempo_bike = parse_float(request.form.get("tempo_bike_horas")) + parse_float(request.form.get("tempo_bike_minutos")) / 60
        tempo_corrida = parse_float(request.form.get("tempo_corrida_horas")) + parse_float(request.form.get("tempo_corrida_minutos")) / 60
        tempo_total = tempo_natacao + tempo_bike + tempo_corrida

        novo_resumo = ResumoSalvo(
            user_id=current_user.id,
            nome_treino=form.nome_treino.data,
            data=form.data.data,
            comentario=form.comentario.data,
            resumo_dados=json.loads(request.form["resumo_dados"]),
            tempo_natacao=tempo_natacao,
            tempo_bike=tempo_bike,
            tempo_corrida=tempo_corrida,
            tempo_total=tempo_total
        )

        database.session.add(novo_resumo)
        database.session.commit()
        flash("Resumo salvo com sucesso!", "success")
        return redirect(url_for('resumo_view'))

    return render_template("salvar_resumo.html", form=form, dados=json.loads(resumo_json))



@app.route('/resumos')
@login_required
def listar_resumos():
    resumos = ResumoSalvo.query.filter_by(user_id=current_user.id).order_by(ResumoSalvo.criado_em.desc()).all()
    return render_template('resumos.html', resumos=resumos)



@app.route('/deletar_resumo/<int:id>', methods=['POST'])
@login_required
def deletar_resumo(id):
    resumo = ResumoSalvo.query.get_or_404(id)
    if resumo.user_id != current_user.id:
        flash("Você não tem permissão para excluir esse resumo.", "danger")
        return redirect(url_for('resumo_view'))

    database.session.delete(resumo)
    database.session.commit()
    flash("Resumo excluído com sucesso!", "success")
    return redirect(url_for('resumo_view'))