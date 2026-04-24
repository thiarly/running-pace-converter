from flask import flash
from conversor.schema import RESUMO_SCHEMA


def agrupar_por_categoria(dados):
    resultado = {}

    for categoria, campos in RESUMO_SCHEMA.items():
        resultado[categoria] = {}

        for chave, meta in campos.items():
            label = meta["label"]
            resultado[categoria][label] = dados.get(chave, 0)

    return resultado


def calcular_totais_planejamento(itens):
    totais = {
        'carbo': 0, 'proteina': 0, 'fibras_alimentares': 0, 'gordura_saturada': 0,
        'sodio': 0, 'magnesio': 0, 'potassio': 0, 'calcio': 0,
        'cafeina': 0, 'taurina': 0, 'beta_alanina': 0, 'citrulina': 0, 'creatina': 0, 'coq10': 0, 'carnitina': 0,
        'leucina': 0, 'isoleucina': 0, 'valina': 0, 'arginina': 0,                           
        'vit_b1': 0, 'vit_b2': 0, 'vit_b3': 0, 'vit_b6': 0,
        'vit_b7': 0, 'vit_b9': 0, 'vit_b12': 0, 'vit_c': 0, 'vit_e': 0, 'vit_ferro': 0, 'vit_d': 0, 'acido_pantotenico': 0, 'acido_folico': 0, 'tirosina': 0, 'colina': 0
    }
    
            
    
# carbo e fibra
    for item in itens:
        suplemento = item.suplemento
        if suplemento is None:
            flash("Um suplemento usado neste planejamento foi removido e será ignorado.", "warning")
            continue

        for key in totais:
            valor = getattr(suplemento, key, 0) or 0
            totais[key] += valor * item.quantidade

    return totais