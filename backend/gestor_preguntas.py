import json
import os

from pregunta import Pregunta
from utilidades import limpiar_pantalla

PREGUNTAS_FILE = ".\\backend\\preguntas.json"

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
        
def agregar_preguntas():
    #parte = input("\nParte temario (especifica | general): ")
    tema = int(input("\nNúmero del tema: "))
    preguntas = cargar_preguntas()
    continuar = True
    while continuar:
        limpiar_pantalla()
        enunciado = input("\nIntroduce el enunciado:\n")
        opciones = [input(f"\nOpción {i+1}: ") for i in range(4)]
        respuesta = int(input("\n¿Cuál es la respuesta correcta? (1-4): ")) - 1
        while not respuesta == 0 and not respuesta == 1 and not respuesta == 2 and not respuesta == 3:
            respuesta = int(input("\n¿Cuál es la respuesta correcta? (1-4): ")) - 1  
        
        nueva = Pregunta(
            id=preguntas[-1].id + 1 if preguntas else 1,
            enunciado=enunciado,
            opciones=opciones,
            respuesta_correcta=respuesta,
            tema=tema
        )
    
        preguntas.append(nueva)
        aux = input("\n¿Desea introducir otra pregunta? (s/n): ")
        while aux != "s" and aux != "n":
            print("\nOpción inválida.")
            aux = input("\n¿Desea introducir otra pregunta? (s/n): ")
        
        if aux == "s":
            continuar = True
        elif aux == "n":
            continuar = False
        
        guardar_preguntas(preguntas)
    
    print("\nPregunta/s añadida/s correctamente.")

def importar_preguntas(archivo):
    try:
        with open(archivo, "r", encoding="utf-8") as file:
            nuevas = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("\nArchivo no encontrado o formato inválido.")
        return
    
    nuevas_preguntas = [Pregunta.from_dict(p) for p in nuevas]
    
    if not os.path.exists(PREGUNTAS_FILE):
        actuales = []
    else:
        try:
            with open(PREGUNTAS_FILE, "r", encoding="utf-8") as file:
                actuales = [Pregunta.from_dict(p) for p in json.load(file)]
        except json.JSONDecodeError:
            actuales = []
            
    max_id = max((p.id for p in actuales), default=0)
    
    for i, p in enumerate(nuevas_preguntas):
        p.id = max_id + i + 1

    todas = actuales + nuevas_preguntas
    
    with open(PREGUNTAS_FILE, "w", encoding="utf-8") as file:
        json.dump([p.to_dict() for p in todas], file, indent=4, ensure_ascii=False)
        
    print("\nSe han importado todas las preguntas.")