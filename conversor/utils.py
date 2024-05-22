def convert_pace(time, distance):
    time_minutes = time // 60  # Obter a parte inteira dos minutos
    time_seconds = time % 60  # Obter os segundos restantes

    total_minutes = time_minutes + time_seconds / 60  # Tempo total em minutos

    pace_km = total_minutes / distance
    pace_mile = total_minutes / (distance / 1.60934)

    pace_km_minutes, pace_km_seconds = divmod(int(pace_km * 60), 60)
    pace_mile_minutes, pace_mile_seconds = divmod(int(pace_mile * 60), 60)

    pace_km_formatted = f'{pace_km_minutes:02d}:{pace_km_seconds:02d} /km'
    pace_mile_formatted = f'{pace_mile_minutes:02d}:{pace_mile_seconds:02d} /milha'

    return pace_km_formatted, pace_mile_formatted


def calc_average_speed_bike(time, distance):
    avg_speed = distance / (time / 3600) # Converter o tempo de segundos para horas
    return f'{avg_speed:.2f}'

def calc_swim_pace(time, distance):
    pace_100m = (time / distance) * 100
    pace_100m_min, pace_100m_sec = divmod(pace_100m, 60)  # Converter para minutos e segundos

    pace_100m_formatted = f'{int(pace_100m_min)}:{int(pace_100m_sec):02d}'  # Formato MM:SS
    return pace_100m_formatted


def calculate_estimated_distance(time, pace):
    pace_min, pace_sec = map(int, pace.split(':'))
    pace_total_seconds = pace_min * 60 + pace_sec
    estimated_distance = time / pace_total_seconds
    return round(estimated_distance, 2)



def calculate_estimated_time(distance, pace):
    pace_min, pace_sec = map(int, pace.split(':'))
    pace_total_seconds = pace_min * 60 + pace_sec
    estimated_time_seconds = distance * pace_total_seconds

    estimated_hours = estimated_time_seconds // 3600
    estimated_minutes = (estimated_time_seconds % 3600) // 60
    estimated_seconds = estimated_time_seconds % 60

    return f'{int(estimated_hours):02}:{int(estimated_minutes):02}:{int(estimated_seconds):02}'



# Conversor de ritmo para velocidade

def convert_pace_to_speed(pace):
    pace_min, pace_sec = map(int, pace.split(':'))
    pace_total_minutes = pace_min + pace_sec / 60
    speed_kmh = 60 / pace_total_minutes
    return round(speed_kmh, 2)


def convert_speed_to_pace(speed_kmh):
    pace_total_minutes = 60 / speed_kmh
    pace_min = int(pace_total_minutes)
    pace_sec = int((pace_total_minutes - pace_min) * 60)
    return f'{pace_min:02}:{pace_sec:02}'


def convert_milha_pace(pace_km):
    pace_min, pace_sec = map(int, pace_km.split(':'))
    pace_total_minutes = pace_min + pace_sec / 60
    pace_total_minutes_mile = pace_total_minutes / 1.60934  # 1 milha = 1.60934 km
    pace_mile_min = int(pace_total_minutes_mile)
    pace_mile_sec = int((pace_total_minutes_mile - pace_mile_min) * 60)
    return f'{pace_mile_min:02}:{pace_mile_sec:02}'


def convert_pace_milha(pace_km):
    pace_min, pace_sec = map(int, pace_km.split(':'))
    pace_total_minutes = pace_min + pace_sec / 60
    pace_total_minutes_mile = pace_total_minutes * 1.60934  # Convertendo pace de km para milha
    pace_mile_min = int(pace_total_minutes_mile)
    pace_mile_sec = int((pace_total_minutes_mile - pace_mile_min) * 60)
    return f'{pace_mile_min:02}:{pace_mile_sec:02}'


def convert_km_to_miles(km):
    miles = km / 1.60934  # 1 milha = 1.60934 km
    return round(miles, 2)


def convert_miles_to_km(miles):
    km = miles * 1.60934  # 1 milha = 1.60934 km
    return round(km, 2)


# Calculadora de VO2Max

def calculate_pace_km(time_seconds, distance_km):
    pace_seconds_per_km = time_seconds / distance_km
    pace_minutes = int(pace_seconds_per_km // 60)
    pace_seconds = int(pace_seconds_per_km % 60)
    return f"{pace_minutes:02}:{pace_seconds:02}"


def calculate_vo2max(time_seconds, distance_km):
    velocity_m_per_s = distance_km * 1000 / time_seconds
    vo2max = (velocity_m_per_s - 5.2) * 1000 / (distance_km / 1.609344)
    return round(vo2max, 1)

def calculate_paces_by_vo2max(pace_seconds_per_km):
    paces = {
        "leve": pace_seconds_per_km / 0.68,
        "moderado": pace_seconds_per_km / 0.76,
        "forte": pace_seconds_per_km / 0.84,
        "muito_forte": pace_seconds_per_km / 0.92,
        "fortissimo": pace_seconds_per_km / 1.0,
        "pra_morte": pace_seconds_per_km / 1.08
    }
    
    return {key: f"{int(pace // 60):02}:{int(pace % 60):02}" for key, pace in paces.items()}


def riegel_prediction(base_time_seconds, base_distance_km, target_distance_km):
    exponent = 1.06
    predicted_time_seconds = base_time_seconds * (target_distance_km / base_distance_km) ** exponent
    return predicted_time_seconds


def race_predictions(time_seconds, distance_km):
    predictions = {
        "3 km": riegel_prediction(time_seconds, distance_km, 3),
        "5 km": riegel_prediction(time_seconds, distance_km, 5),
        "10 km": time_seconds,
        "meia": riegel_prediction(time_seconds, distance_km, 21.0975),
        "maratona": riegel_prediction(time_seconds, distance_km, 42.195)
    }
    
    return {key: f"{int(pred // 3600):02}:{int((pred % 3600) // 60):02}:{int(pred % 60):02}" for key, pred in predictions.items()}



def race_predictions_from_3k(time_seconds, distance_km):
    distance_mapping = {
        "3 km": 3,
        "5 km": 5,
        "10 km": 10,
        "meia": 21.0975,
        "maratona": 42.195
    }
    
    predictions = {
        "3 km": time_seconds,
        "5 km": riegel_prediction(time_seconds, distance_km, 5),
        "10 km": riegel_prediction(time_seconds, distance_km, 10),
        "meia": riegel_prediction(time_seconds, distance_km, 21.0975),
        "maratona": riegel_prediction(time_seconds, distance_km, 42.195)
    }

    # Calculando o pace para cada previsão
    prediction_paces = {
        key: calculate_pace_km(pred, distance_mapping[key])
        for key, pred in predictions.items()
    }

    # Agrupando as previsões e paces
    formatted_predictions = {
        key: {
            'Tempo': f"{int(pred // 3600):02}:{int((pred % 3600) // 60):02}:{int(pred % 60):02}",
            'Pace': prediction_paces[key]
        }
        for key, pred in predictions.items()
    }
    
    return formatted_predictions
