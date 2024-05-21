from flask import Flask, render_template, request
from conversor import app
from conversor.utils import convert_pace, calc_average_speed_bike, calc_swim_pace, calculate_estimated_time, calculate_estimated_distance, convert_pace_to_speed, convert_speed_to_pace, convert_milha_pace, convert_pace_milha

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


@app.route('/zonas')
def zonas():
    return render_template('zonas.html')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')