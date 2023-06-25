from flask import Flask, render_template, request
from runnerpacer import app
from runnerpacer.utils import convert_pace, calc_average_speed_bike, calc_swim_pace

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        hour = int(request.form.get('hour'))
        minute = int(request.form.get('minute'))
        second = int(request.form.get('second'))
        distance = float(request.form.get('distance'))
        activity = request.form.get('activity')

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

    return render_template('home.html')


@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/moeda')
def moeda():
    return render_template('moeda.html')





