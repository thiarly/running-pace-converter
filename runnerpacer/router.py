from flask import Flask, render_template, request
from runnerpacer import app

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        hour = int(request.form.get('hour'))
        minute = int(request.form.get('minute'))
        second = int(request.form.get('second'))
        distance = float(request.form.get('distance'))
        activity = request.form.get('activity')

        time = hour * 3600 + minute * 60 + second  # Converter o tempo total em segundos

        if activity == 'corrida':
            pace_km, pace_mile = convert_pace(time, distance)
            return render_template('index.html', pace_km=pace_km, pace_mile=pace_mile)
        
        elif activity == 'ciclismo':
            avg_speed = calc_average_speed_bike(time, distance)
            return render_template('index.html', avg_speed=avg_speed)

        elif activity == 'natacao':
            pace_100m = calc_swim_pace(time, distance)
            return render_template('index.html', pace_100m=pace_100m)

    return render_template('index.html')




def convert_pace(time, distance):
    time_minutes = time // 60  # Obter a parte inteira dos minutos
    time_seconds = time % 60  # Obter os segundos restantes

    total_minutes = time_minutes + time_seconds / 60  # Tempo total em minutos

    pace_km = total_minutes / distance
    pace_mile = total_minutes / (distance / 1.60934)

    pace_km_minutes, pace_km_seconds = divmod(int(pace_km * 60), 60)
    pace_mile_minutes, pace_mile_seconds = divmod(int(pace_mile * 60), 60)

    pace_km_formatted = f'{pace_km_minutes:02d}:{pace_km_seconds:02d} /km'
    pace_mile_formatted = f'{pace_mile_minutes:02d}:{pace_mile_seconds:02d} /mile'

    return pace_km_formatted, pace_mile_formatted


def convert_pace_mile(time, distance):
    pace_mile = time / (distance / 1.60934)

    pace_mile_minutes, pace_mile_seconds = divmod(int(pace_mile * 60), 60)

    pace_mile_formatted = f'{pace_mile_minutes:02d}:{pace_mile_seconds:02d} /mile'

    return pace_mile_formatted


def calc_average_speed_bike(time, distance):
    avg_speed = distance / (time / 3600) # Converter o tempo de segundos para horas
    return f'{avg_speed:.2f}'

def calc_swim_pace(time, distance):
    pace_100m = (time / distance) * 100
    pace_100m_min, pace_100m_sec = divmod(pace_100m, 60)  # Converter para minutos e segundos

    pace_100m_formatted = f'{int(pace_100m_min)}:{pace_100m_sec:02d}'  # Formato MM:SS
    return pace_100m_formatted
