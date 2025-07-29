import random
import datetime
import json
import os

from gestor_preguntas import cargar_preguntas

RESULTADOS_FILE = "resultados.json"
NUMERO_PREGUNTAS = 5

def guardar_resultado(aciertos, fallos, nota, duracion, fecha):
    resultado = {
        "duracion_segundos": duracion.total_seconds(),
        "aciertos": aciertos,
        "fallos": fallos,
        "nota": nota
    }
    
    if not os.path.exists(RESULTADOS_FILE):
        resultados = []
    else:
        try:
            with open(RESULTADOS_FILE, "r", encoding="utf-8") as file:
                resultados = json.load(file)
        except json.JSONDecodeError:
            resultados = []
    
    resultados.append(resultado)
    with open(RESULTADOS_FILE, "w", encoding="utf-8") as file:
        json.dump(resultados, file, indent=4, ensure_ascii=False)
        
def hacer_examen(tema):
    preguntas = cargar_preguntas()
    p_filtradas = [p for p in preguntas if p.tema == tema]
    if len(p_filtradas) < NUMERO_PREGUNTAS:
        print("\nNo hay suficientes preguntas")
        return
    seleccionadas = random.sample(p_filtradas, NUMERO_PREGUNTAS)
    aciertos = 0
    fallos = 0
    nota = 0
    
    inicio = datetime.datetime.now()
    
    for i, p in enumerate(seleccionadas):
        print(f"\n{i+1}. {p.enunciado}")
        for j, op in enumerate(p.opciones):
            print(f"    {j+1}. {op}")
        r = int(input("Tu respuesta (1-4): ")) - 1
        if r == p.respuesta_correcta:
            print("\n¡Correcto!")
            aciertos += 1
        else:
            print(f"\nIncorrecto.\n\nLa respuesta correcta es:\n{p.opciones[p.respuesta_correcta]}")
            fallos += 1
            
    fin = datetime.datetime.now()  
    duracion = fin - inicio     
    nota = round((aciertos - (fallos / 3)) / NUMERO_PREGUNTAS, 2) * 10
    
    print(f"\nAciertos: {aciertos}.\nFallos: {fallos}.\nNota final: {nota}.\nTiempo: {duracion}")
    guardar_resultado(aciertos, fallos, nota, duracion, inicio)