def segundos_para_hms(segundos):
    segundos = int(round(segundos))
    h = segundos // 3600
    m = (segundos % 3600) // 60
    s = segundos % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


def segundos_para_mmss(segundos):
    segundos = int(round(segundos))
    m = segundos // 60
    s = segundos % 60
    return f"{m:02d}:{s:02d}"


def pace_para_segundos(pace):
    minutos, segundos = pace.split(":")
    return int(minutos) * 60 + int(segundos)


def tempo_para_segundos(hour=0, minute=0, second=0):
    return int(hour or 0) * 3600 + int(minute or 0) * 60 + int(second or 0)