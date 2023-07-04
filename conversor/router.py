from flask import Flask, render_template, request
from conversor import app
from conversor.utils import convert_pace, calc_average_speed_bike, calc_swim_pace

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



@app.route('/zonas')
def zonas():
    return render_template('zonas.html')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')