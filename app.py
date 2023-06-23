from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        time = float(request.form.get('time'))
        distance = float(request.form.get('distance'))
        activity = request.form.get('activity')

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
    pace_km = time / distance
    pace_mile = time / (distance / 1.60934)

    pace_km_min, pace_km_sec = divmod(pace_km, 1)
    pace_mile_min, pace_mile_sec = divmod(pace_mile, 1)

    pace_km_formatted = f'{int(pace_km_min)}:{float(pace_km_sec*60)}'
    pace_mile_formatted = f'{int(pace_mile_min)}:{float(pace_mile_sec*60)}'
    
    return pace_km_formatted, pace_mile_formatted

def calc_average_speed_bike(time, distance):
    avg_speed = distance / (time / 60)
    return f'{avg_speed:.2f} km/h'

def calc_swim_pace(time, distance):
    pace_100m = (time / distance) * 100
    pace_100m_min, pace_100m_sec = divmod(pace_100m, 1)

    pace_100m_formatted = f'{int(pace_100m_min)}:{pace_100m_sec*60:.2f}'
    return pace_100m_formatted

if __name__ == '__main__':
    app.run(debug=True)
