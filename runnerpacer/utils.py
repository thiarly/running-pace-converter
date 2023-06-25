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
