import json
import os

from pregunta import Pregunta
from utilidades import limpiar_pantalla

def cargar_preguntas(tema):
    archivo_preguntas = ".\\data\\preguntas\\preguntas_tema_" + str(tema) + ".json"
    
    # Comprobamos la existencia del archivo
    if not os.path.exists(archivo_preguntas):
        with open(archivo_preguntas, "w", encoding="utf-8") as file:
            json.dump([], file)
        return []
    
    # Abrimos el archivo de preguntas
    try:
        with open(archivo_preguntas, "r", encoding="utf-8") as file:
            datos = json.load(file)
            
    except json.JSONDecodeError:
        with open(archivo_preguntas, "w", encoding="utf-8") as file:
            json.dump([], file)
        return []
    
    return [Pregunta.from_dict(p) for p in datos]
    
def guardar_preguntas(preguntas, tema):
    examen_file = ".\\data\\preguntas\\preguntas_tema_" + str(tema) + ".json"
    with open(examen_file, "w", encoding="utf-8") as file:
        json.dump([p.to_dict() for p in preguntas], file, indent=4, ensure_ascii=False)
        
def agregar_pregunta():  
    # Cargamos todas las preguntas del tema escogido
    tema = int(input("\nNúmero del tema: "))
    while 0 < tema > 35:
        print("\nTema incorrecto.")
        tema = input("\nNúmero del tema: ")
    preguntas = cargar_preguntas(tema)
    continuar = True
    
    # Bucle para introducir preguntas
    while continuar:
        limpiar_pantalla()
        
        # Pedimos los datos de la pregunta
        enunciado = input("\nIntroduce el enunciado:\n")
        opciones_texto = [input(f"\nOpción {i+1}: ") for i in range(4)]
        respuesta = int(input("\n¿Cuál es la respuesta correcta? (1-4): ")) - 1
        while respuesta < 0 or respuesta > 3:
            print("\nOpción incorrecta.")
            respuesta = int(input("\n¿Cuál es la respuesta correcta? (1-4): ")) - 1
        
        # Añadimos la respuesta correcta
        opciones = []
        for i in range(4):
            opciones.append({
                'texto': opciones_texto[i],
                'correcta': (i == respuesta)
            })
                        
        # Creamos el objeto de la pregunta y la guardamos
        nueva = Pregunta(
            id=preguntas[-1].id + 1 if preguntas else 1,
            enunciado=enunciado,
            opciones=opciones
        )
        
        preguntas.append(nueva)
        guardar_preguntas(preguntas, tema)
        
        # Condicional salida del bucle
        aux = input("\n¿Desea introducir otra pregunta? (s/n): ")
        while aux != "s" and aux != "n":
            print("\nOpción inválida.")
            aux = input("\n¿Desea introducir otra pregunta? (s/n): ")   
        if aux == "s":
            continuar = True
        elif aux == "n":
            continuar = False
            
    print("\nPregunta/s añadida/s correctamente.")

def importar_preguntas():
    # Cargamos las preguntas del tema
    tema = int(input("\nNúmero del tema: "))
    while 0 < tema > 35:
        print("\nTema incorrecto.")
        tema = input("\nNúmero del tema: ")
    preguntas = cargar_preguntas(tema)
    
    archivo = "preguntas_nuevas.json"
    try:
        with open(archivo, "r", encoding="utf-8") as file:
            nuevas = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("\nArchivo no encontrado o formato inválido.")
        return 
    
    nuevas_preguntas = [Pregunta.from_dict(p) for p in nuevas]
            
    max_id = max((p.id for p in preguntas), default=0)
    
    for i, p in enumerate(nuevas_preguntas):
        p.id = max_id + i + 1

    todas = preguntas + nuevas_preguntas
    
    guardar_preguntas(todas, tema)
    
    print("\nSe han importado todas las preguntas.")
    