import json
import os

from pregunta import Pregunta

PREGUNTAS_FILE = "preguntas.json"

def cargar_preguntas():
    if not os.path.exists(PREGUNTAS_FILE):
        with open(PREGUNTAS_FILE, "w", encoding="utf-8") as file:
            json.dump([], file)
        return []
    
    try:
        with open(PREGUNTAS_FILE, "r", encoding="utf-8") as file:
            datos = json.load(file)
    
    except json.JSONDecodeError:
        with open(PREGUNTAS_FILE, "w", encoding="utf-8") as file:
            json.dump([], file)
        return []
    
    return [Pregunta.from_dict(p) for p in datos]
    
def guardar_preguntas(preguntas):
    with open(PREGUNTAS_FILE, "w", encoding="utf-8") as file:
        json.dump([p.to_dict() for p in preguntas], file, indent=4, ensure_ascii=False)
        
def agregar_pregunta():
    enunciado = input("\nIntroduce el enunciado: ")
    opciones = [input(f"\nOpción {i+1}: ") for i in range(4)]
    respuesta = int(input("\n¿Cuál es la respuesta correcta? (1-4): ")) - 1
    while not respuesta == 0 and not respuesta == 1 and not respuesta == 2 and not respuesta == 3:
        respuesta = int(input("\n¿Cuál es la respuesta correcta? (1-4): ")) - 1
    #tema = int(input("\nNúmero del tema: "))
    tema = 6
    preguntas = cargar_preguntas()
    
    nueva = Pregunta(
        id=preguntas[-1].id + 1 if preguntas else 1,
        enunciado=enunciado,
        opciones=opciones,
        respuesta_correcta=respuesta,
        tema=tema
    )
    
    preguntas.append(nueva)
    guardar_preguntas(preguntas)
    print("\nPregunta añadida correctamente.")
    
    