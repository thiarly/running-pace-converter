from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from conversor import app, database

from conversor.forms import SuplementoForm, PlanningItemForm, ResumoForm, LoginForm, RegisterForm, ResumoForm, SalvarResumoForm
from conversor.models import Suplemento, PlanejamentoItem, User, ResumoSalvo

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, logout_user

import json
from datetime import date

import os

from conversor.utils import (
    convert_pace, calc_average_speed_bike,
    calc_swim_pace, calculate_estimated_time,
    calculate_estimated_distance, convert_pace_to_speed,
    convert_speed_to_pace, convert_milha_pace,
    convert_pace_milha, convert_km_to_miles,
    convert_miles_to_km, calculate_vo2max,
    race_predictions, calculate_pace_km, calculate_paces_by_vo2max,
    race_predictions_from_3k, agrupar_por_categoria,
    calcular_zonas_ftp, calcular_zonas_fc, calcular_zonas_pace,
    calcular_totais_planejamento
)





@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.senha_hash, form.senha.data):
            login_user(user, remember=True)
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
    distance = ''
    pace = ''
    estimated_time = None
    error = None

    if request.method == 'POST':
        distance = request.form.get('distance')
        pace = request.form.get('pace')

        if not distance or not pace:
            error = 'Por favor, forneça valores para a distância e o pace.'
        else:
            try:
                distance_float = float(distance)
                estimated_time = calculate_estimated_time(distance_float, pace)
            except ValueError:
                error = 'Distância inválida.'

    return render_template(
        'estimativa_tempo.html',
        estimated_time=estimated_time,
        distance=distance,
        pace=pace,
        error=error
    )


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


@app.route('/zonas/calculadora', methods=['GET', 'POST'])
def calculadora_zonas():
    zonas = None
    metodo = None
    valor = None
    pace_min_km = None

    if request.method == 'POST':
        metodo = request.form.get('metodo')
        valor = request.form.get('valor')

        if metodo == 'ftp':
            try:
                ftp = float(valor)
                zonas = calcular_zonas_ftp(ftp)
            except ValueError:
                zonas = None

        elif metodo == 'fc':
            try:
                fc = float(valor)
                zonas = calcular_zonas_fc(fc)
            except ValueError:
                zonas = None

        elif metodo == 'pace':
            try:
                if ':' not in valor:
                    raise ValueError("Formato inválido")
                minutos, segundos = map(int, valor.strip().split(':'))
                pace_threshold = minutos * 60 + segundos
                zonas = calcular_zonas_pace(pace_threshold)
            except (ValueError, AttributeError):
                zonas = None

    return render_template(
        'calculadora_zonas.html',
        zonas=zonas,
        metodo=metodo,
        valor=valor,
        pace_min_km=pace_min_km
    )


@app.route('/zonas')
def zonas():
    return render_template('zonas.html')


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
            ingredientes=form.ingredientes.data,
            comentario=form.comentario.data,
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
    form.suplemento_id.choices = [
        (s.id, s.nome) for s in Suplemento.query.filter_by(user_id=current_user.id)
    ]

    if form.validate_on_submit():
        item_existente = PlanejamentoItem.query.filter_by(
            suplemento_id=form.suplemento_id.data, user_id=current_user.id
        ).first()
        if item_existente:
            item_existente.quantidade += float(form.quantidade.data)
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

    # 🔽 Limpa automaticamente os itens com suplemento excluído
    itens = PlanejamentoItem.query.filter_by(user_id=current_user.id).all()
    itens_validos = []

    for item in itens:
        if item.suplemento is None:
            database.session.delete(item)
        else:
            itens_validos.append(item)

    database.session.commit()  # aplica exclusões
    totais = calcular_totais_planejamento(itens_validos)

    return render_template('planejamento.html', form=form, itens=itens_validos, totais=totais)



# Atualizar quantidade no planejamento
@app.route('/planejamento/atualizar/<int:item_id>', methods=['POST'])
@login_required
def atualizar_quantidade(item_id):
    item = PlanejamentoItem.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()

    try:
        # Aceita ponto ou vírgula como separador decimal
        quantidade_str = request.form.get('quantidade', '').replace(',', '.')
        nova_quantidade = float(quantidade_str)

        if nova_quantidade >= 0.01:
            item.quantidade = nova_quantidade
            database.session.commit()
            flash('Quantidade atualizada com sucesso!', 'success')
        else:
            flash('Quantidade inválida.', 'danger')

    except (ValueError, TypeError):
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

# Remover todos os itens do planejamento
@app.route('/planejamento/remover_todos', methods=['POST'])
@login_required
def remover_todos_itens():
    PlanejamentoItem.query.filter_by(user_id=current_user.id).delete()
    database.session.commit()
    flash('Todos os itens foram removidos do planejamento.', 'success')
    return redirect(url_for('planejamento'))


# Resumo
@app.route('/resumo', methods=['GET', 'POST'])
@login_required
def resumo_view():
    form = ResumoForm()

    if request.method == 'POST' and 'limpar' in request.form:
        return redirect(url_for('resumo_view'))

    itens = PlanejamentoItem.query.filter_by(user_id=current_user.id).all()
    itens_utilizados = [f"{item.quantidade}x {item.suplemento.nome}" for item in itens if item.suplemento]
    itens_utilizados_str = ", ".join(itens_utilizados)


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
    search = request.args.get("search", "").strip()

    resumos_query = ResumoSalvo.query.filter_by(user_id=current_user.id)

    if search:
        resumos_query = resumos_query.filter(
            database.or_(
                ResumoSalvo.nome_treino.ilike(f"%{search}%"),
                ResumoSalvo.comentario.ilike(f"%{search}%")
            )
        )

    resumos = resumos_query.order_by(ResumoSalvo.ordem.desc(), ResumoSalvo.id.desc()).all()

    

    return render_template(
        "resumo.html",
        form=form,
        totais=totais_por_hora,
        resumo=resumo_dados,
        tempo_total=round(tempo_total, 2),
        current_date=date.today().isoformat(),
        resumos=resumos,  # <-- novo contexto
        itens_utilizados=itens_utilizados_str
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

        # 🔽 Captura os suplementos utilizados no momento atual
        itens = PlanejamentoItem.query.filter_by(user_id=current_user.id).all()
        suplementos_utilizados = ", ".join(
            [f"{item.quantidade}x {item.suplemento.nome}" for item in itens if item.suplemento]
        )

        novo_resumo = ResumoSalvo(
            user_id=current_user.id,
            nome_treino=form.nome_treino.data,
            data=form.data.data,
            comentario=form.comentario.data,
            resumo_dados=json.loads(request.form["resumo_dados"]),
            suplementos_utilizados=suplementos_utilizados,  # ✅ aqui
            tempo_natacao=tempo_natacao,
            tempo_bike=tempo_bike,
            tempo_corrida=tempo_corrida,
            tempo_total=tempo_total
        )

        # Define a maior ordem atual + 1
        maior_ordem = database.session.query(database.func.max(ResumoSalvo.ordem)).filter_by(user_id=current_user.id).scalar() or 0
        novo_resumo.ordem = maior_ordem + 1
            
        database.session.add(novo_resumo)
        database.session.commit()
        flash("Resumo salvo com sucesso!", "success")
        return redirect(url_for('resumo_view'))

    return render_template("salvar_resumo.html", form=form, dados=json.loads(resumo_json))


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


@app.route('/buscar_resumos')
@login_required
def buscar_resumos():
    termo = request.args.get("termo", "").strip().lower()

    query = ResumoSalvo.query.filter_by(user_id=current_user.id)

    if termo:
        query = query.filter(
            database.or_(
                ResumoSalvo.nome_treino.ilike(f"%{termo}%"),
                ResumoSalvo.comentario.ilike(f"%{termo}%")
            )
        )

    resultados = query.order_by(ResumoSalvo.data.desc()).all()

    return jsonify([
        {
            "id": r.id,
            "nome_treino": r.nome_treino,
            "comentario": r.comentario,
            "data": r.data.strftime("%d/%m/%Y"),
            "tempo_total": round(r.tempo_total, 2),
            "tempo_natacao": round(r.tempo_natacao, 2),
            "tempo_bike": round(r.tempo_bike, 2),
            "tempo_corrida": round(r.tempo_corrida, 2),
            "resumo_dados": r.resumo_dados  # ⬅️ aqui está a chave
        }
        for r in resultados
    ])



@app.route('/resumo/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_resumo(id):
    resumo = ResumoSalvo.query.get_or_404(id)
    if resumo.user_id != current_user.id:
        flash("Você não tem permissão para editar esse resumo.", "danger")
        return redirect(url_for('resumo_view'))

    form = SalvarResumoForm(obj=resumo)

    if form.validate_on_submit():
        resumo.nome_treino = form.nome_treino.data
        resumo.data = form.data.data
        resumo.comentario = form.comentario.data

        # opcionalmente você pode reprocessar tempos ou suplementos aqui
        database.session.commit()
        flash("Resumo atualizado com sucesso!", "success")
        return redirect(url_for('resumo_view'))

    return render_template("editar_resumo.html", form=form, resumo=resumo)



# 🔼 mover_cima (ordem maior → menor)
@app.route('/resumo/mover_cima/<int:id>')
@login_required
def mover_cima(id):
    atual = ResumoSalvo.query.get_or_404(id)
    anterior = ResumoSalvo.query.filter(
        ResumoSalvo.user_id == current_user.id,
        ResumoSalvo.ordem > atual.ordem
    ).order_by(ResumoSalvo.ordem.asc()).first()

    if anterior:
        atual.ordem, anterior.ordem = anterior.ordem, atual.ordem
        database.session.commit()

    return redirect(url_for('resumo_view'))


# 🔽 mover_baixo (ordem menor → maior)
@app.route('/resumo/mover_baixo/<int:id>')
@login_required
def mover_baixo(id):
    atual = ResumoSalvo.query.get_or_404(id)
    proximo = ResumoSalvo.query.filter(
        ResumoSalvo.user_id == current_user.id,
        ResumoSalvo.ordem < atual.ordem
    ).order_by(ResumoSalvo.ordem.desc()).first()

    if proximo:
        atual.ordem, proximo.ordem = proximo.ordem, atual.ordem
        database.session.commit()

    return redirect(url_for('resumo_view'))



@app.route('/salvar_resumo_livre', methods=['POST'])
@login_required
def salvar_resumo_livre():
    form = SalvarResumoForm()

    itens = PlanejamentoItem.query.filter_by(user_id=current_user.id).all()
    suplementos_utilizados = ", ".join(
        [f"{item.quantidade}x {item.suplemento.nome}" for item in itens if item.suplemento]
    )

    resumo_dados = agrupar_por_categoria(calcular_totais_planejamento(itens))  # total bruto

    novo_resumo = ResumoSalvo(
        user_id=current_user.id,
        nome_treino=form.nome_treino.data,
        data=form.data.data,
        comentario=form.comentario.data,
        resumo_dados=resumo_dados,
        suplementos_utilizados=suplementos_utilizados,
        tempo_natacao=0,
        tempo_bike=0,
        tempo_corrida=0,
        tempo_total=0,
        ordem=(database.session.query(database.func.max(ResumoSalvo.ordem))
               .filter_by(user_id=current_user.id).scalar() or 0) + 1
    )

    database.session.add(novo_resumo)
    database.session.commit()
    flash("Resumo livre salvo com sucesso!", "success")
    return redirect(url_for('resumo_view'))


#