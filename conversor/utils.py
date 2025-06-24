from flask import flash

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


def race_predictions_formatted(time_seconds, distance_km):
    distance_mapping = {
        "3 km": 3,
        "5 km": 5,
        "10 km": 10,
        "meia": 21.0975,
        "maratona": 42.195
    }

    predictions = {
        prova: riegel_prediction(time_seconds, distance_km, dist)
        for prova, dist in distance_mapping.items()
    }

    prediction_paces = {
        prova: calculate_pace_km(predictions[prova], dist)
        for prova, dist in distance_mapping.items()
    }

    return {
        prova: {
            'Tempo': f"{int(pred // 3600):02}:{int((pred % 3600) // 60):02}:{int(pred % 60):02}",
            'Pace': prediction_paces[prova]
        }
        for prova, pred in predictions.items()
    }

def calculate_vo2max(time_seconds):
    # Converte segundos totais em pace por km
    pace_segundos = time_seconds / 10  # considerando 10 km

    # Velocidade média em km/h
    velocidade_kmh = 3600 / pace_segundos

    # Fórmula estimada de VO2max baseada na velocidade (Garmin/Polar)
    vo2max = 3.5 + 12 * (velocidade_kmh / 3.5)

    # Cálculo das zonas baseadas no pace de referência
    zonas = {
        "Z1 (Leve - 50% a 60%)": (pace_segundos / 0.50, pace_segundos / 0.60),
        "Z2 (Endurance - 60% a 70%)": (pace_segundos / 0.60, pace_segundos / 0.70),
        "Z3 (Tempo - 70% a 80%)": (pace_segundos / 0.70, pace_segundos / 0.80),
        "Z4 (Limiar - 80% a 90%)": (pace_segundos / 0.80, pace_segundos / 0.90),
        "Z5 (VO2Max - 90% a 100%)": (pace_segundos / 0.90, pace_segundos / 1.00),
    }

    # Formatando os paces das zonas para MM:SS
    zonas_formatadas = {
        nome: f"{int(maximo // 60):02d}:{int(maximo % 60):02d} → {int(minimo // 60):02d}:{int(minimo % 60):02d}"
        for nome, (minimo, maximo) in zonas.items()
    }

    return {
        "pace": f"{int(pace_segundos // 60):02d}:{int(pace_segundos % 60):02d}",
        "vo2max": round(vo2max, 1),
        "zonas": zonas_formatadas
    }


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


def agrupar_por_categoria(dados):
    return {
        "Macronutrientes": {
            "Carboidrato": dados.get("carbo", 0),
        },
        "Eletrólitos": {
            "Sódio": dados.get("sodio", 0),
            "Magnésio": dados.get("magnesio", 0),
            "Potássio": dados.get("potassio", 0),
            "Cálcio": dados.get("calcio", 0),
        },
        "Estimulantes e Compostos": {
            "Cafeína": dados.get("cafeina", 0),
            "Taurina": dados.get("taurina", 0),
            "Beta-Alanina": dados.get("beta_alanina", 0),
            "Citrulina": dados.get("citrulina", 0),
            "Creatina": dados.get("creatina", 0),
            "CoQ10": dados.get("coq10", 0),
            "Carnitina": dados.get("carnitina", 0),
        },
        "Aminoácidos": {
            "Leucina": dados.get("leucina", 0),
            "Isoleucina": dados.get("isoleucina", 0),
            "Valina": dados.get("valina", 0),
            "Arginina": dados.get("arginina", 0),
        },
        "Vitaminas": {
            "Vitamina B1": dados.get("vit_b1", 0),
            "Vitamina B2": dados.get("vit_b2", 0),
            "Vitamina B3": dados.get("vit_b3", 0),
            "Vitamina B6": dados.get("vit_b6", 0),
            "Vitamina B7": dados.get("vit_b7", 0),
            "Vitamina B9": dados.get("vit_b9", 0),
            "Vitamina B12": dados.get("vit_b12", 0),
            "Vitamina C": dados.get("vit_c", 0),
        }
    }
    
    
def calcular_zonas_fc(fc_max):
    return {
        'Zona 1': (0.5 * fc_max, 0.6 * fc_max),
        'Zona 2': (0.6 * fc_max, 0.7 * fc_max),
        'Zona 3': (0.7 * fc_max, 0.8 * fc_max),
        'Zona 4': (0.8 * fc_max, 0.9 * fc_max),
        'Zona 5': (0.9 * fc_max, fc_max)
    }

def calcular_zonas_ftp(ftp):
    return {
        'Zona 1': (0, 0.55 * ftp),
        'Zona 2': (0.56 * ftp, 0.75 * ftp),
        'Zona 3': (0.76 * ftp, 0.90 * ftp),
        'Zona 4': (0.91 * ftp, 1.05 * ftp),
        'Zona 5': (1.06 * ftp, 1.20 * ftp),
        'Zona 6': (1.21 * ftp, 1.50 * ftp),
        'Zona 7': (1.51 * ftp, ftp * 2)
    }
    
    
def calcular_zonas_pace(pace_threshold_segundos):
    zonas = {
        "Zona 1 (Recuperação)": (pace_threshold_segundos * 1.15, pace_threshold_segundos * 1.30),
        "Zona 2 (Endurance)":    (pace_threshold_segundos * 1.00, pace_threshold_segundos * 1.14),
        "Zona 3 (Tempo)":        (pace_threshold_segundos * 0.95, pace_threshold_segundos * 0.99),
        "Zona 4 (Limiar)":       (pace_threshold_segundos * 0.90, pace_threshold_segundos * 0.94),
        "Zona 5 (VO2 Máx)":      (pace_threshold_segundos * 0.80, pace_threshold_segundos * 0.89),
    }

    # Converte os valores de segundos para tuplas (min, seg)
    zonas_formatadas = {}
    for nome, (min_seg, max_seg) in zonas.items():
        zonas_formatadas[nome] = (int(min_seg), int(max_seg))

    return zonas_formatadas



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
        if suplemento is None:
            flash("Um suplemento usado neste planejamento foi removido e será ignorado.", "warning")
            continue

        for key in totais:
            valor = getattr(suplemento, key, 0) or 0
            totais[key] += valor * item.quantidade

    return totais