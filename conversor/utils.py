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
