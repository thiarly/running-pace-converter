from flask import Flask, render_template, request, redirect, url_for, flash
from conversor import app, database

from conversor.forms import SuplementoForm
from conversor.models import Suplemento

from conversor.utils import (
    convert_pace, calc_average_speed_bike,
    calc_swim_pace, calculate_estimated_time,
    calculate_estimated_distance, convert_pace_to_speed,
    convert_speed_to_pace, convert_milha_pace,
    convert_pace_milha, convert_km_to_miles,
    convert_miles_to_km, calculate_vo2max,
    race_predictions, calculate_pace_km, calculate_paces_by_vo2max,
    race_predictions_from_3k
)



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



@app.route('/suplementos/novo', methods=['GET', 'POST'])
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
            vit_c=form.vit_c.data
        )
        db.session.add(suplemento)
        db.session.commit()
        flash('Suplemento cadastrado com sucesso!', 'success')
        return redirect(url_for('novo_suplemento'))
    return render_template('cadastro_suplemento.html', form=form)