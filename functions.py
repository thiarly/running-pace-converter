def convert_pace(time, distance):
    # Calcular o ritmo por km e por milha (1 milha é aproximadamente 1.60934 km)
    pace_km = time / distance
    pace_mile = time / (distance / 1.60934)
    
    # Convertendo para minutos e segundos
    pace_km_min, pace_km_sec = divmod(pace_km, 1)
    pace_mile_min, pace_mile_sec = divmod(pace_mile, 1)
    
    print(f'Pace por quilômetro: {int(pace_km_min)}:{int(pace_km_sec*60)} /km')
    print(f'Pace por milha: {int(pace_mile_min)}:{int(pace_mile_sec*60)} /km')

def calc_average_speed_bike(time, distance):
    # Calcular a velocidade média
    avg_speed = distance / (time / 60)
    
    print('Velocidade média: {:.2f} km/h'.format(avg_speed))

def calc_swim_pace(time, distance):
    # Calcular o ritmo para cada 100m
    pace_100m = (time / distance) * 100
    
    # Convertendo para minutos e segundos
    pace_100m_min, pace_100m_sec = divmod(pace_100m, 1)
    
    print(f'Pace para cada 100m: {int(pace_100m_min)}:{int(pace_100m_sec*60)}s')

# Exemplo de uso
convert_pace(38, 10)
calc_average_speed_bike(54, 35)
calc_swim_pace(15, 1000)
