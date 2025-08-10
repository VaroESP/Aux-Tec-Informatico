import random
import datetime
import json
import os

from gestor_preguntas import cargar_preguntas
from utilidades import pausa, limpiar_pantalla, num_archivos
from examen import Examen

EXAMENES_FILE = ".\\data\\examenes\\examenes.json"
PREGUNTAS_POR_TEMA = 5

def listar_examenes():
    
    # Comprobamos si existe el archivo
    if not os.path.exists(EXAMENES_FILE):
        examenes_data = []
    else:
        # Cargamos los datos existentes
        try:
            with open(EXAMENES_FILE, "r", encoding="utf-8") as file:
                examenes_data = json.load(file)
        except json.JSONDecodeError:
            examenes_data = []
          
    print("\nListado de exámenes:")
    
    for e in examenes_data:
        examen = Examen.from_dict(e)
        print(f"\nID: {examen.id}", end="")
        print(f" | Fecha: {examen.inicio.strftime('%d/%m/%Y') if examen.inicio else 'N/D'}", end="")
        
        duracion_seg = int(examen.duracion.total_seconds()) if examen.duracion else 0
        horas, resto = divmod(duracion_seg, 3600)
        minutos, segundos = divmod(resto, 60)
        
        partes = []
        if horas > 0:
            partes.append(f"{horas}h: ")
        if minutos > 0:
            partes.append(f"{minutos}m: ")
        if segundos > 0 or not partes:
            partes.append(f"{segundos}s")
        duracion_str = " ".join(partes)
        
        print(f" | Duración: {duracion_str}", end="")
        print(f" | Nota: {examen.nota}")

def guardar_examen(preguntas, aciertos, fallos, nota, inicio, duracion):
    
    # Comprobamos si existe el archivo
    if not os.path.exists(EXAMENES_FILE):
        examenes_data = []
    else:
        # Cargamos los datos existentes
        try:
            with open(EXAMENES_FILE, "r", encoding="utf-8") as file:
                examenes_data = json.load(file)
        except json.JSONDecodeError:
            examenes_data = []
    
    # Extraer IDs existentes
    ids = {ex['id'] for ex in examenes_data if 'id' in ex}
    
    # Buscamos el primer ID libre
    nuevo_id = 1
    while nuevo_id in ids:
        nuevo_id += 1
    
    # Creamos el objeto Examen y lo añadimos
    nuevo_examen = Examen(
        id=nuevo_id,
        preguntas=preguntas,
        aciertos=aciertos,
        fallos=fallos,
        nota=nota,
        inicio=inicio,
        duracion=duracion
    )
    examenes_data.append(nuevo_examen.to_dict())
    
    # Escribimos los datos en el archivo
    with open(EXAMENES_FILE, "w", encoding="utf-8") as file:
        json.dump(examenes_data, file, indent=4, ensure_ascii=False)
        
def nuevo_examen():
    preguntas = []
    
    # Sacamos el número de temas disponibles
    ruta = ".\\data\\preguntas"
    numero_temas = num_archivos(ruta)
    for tema in range(numero_temas):
        # Cargamos las preguntas por tema
        preguntas_tema = cargar_preguntas(tema + 1)
        
        # Hacemos una selección aleatoria de preguntas
        preguntas_seleccionadas = random.sample(preguntas_tema, PREGUNTAS_POR_TEMA)
        
        # Añadimos las preguntas seleccionadas
        preguntas.extend(preguntas_seleccionadas)
    
    aciertos = 0
    fallos = 0
    
    # Comenzamos el examen
    inicio = datetime.datetime.now()
    
    for i, p in enumerate(preguntas):
        limpiar_pantalla()
        
        # Mostramos el enunciado
        print(f"\n{i+1}. {p.enunciado}")
        
        # Mostramos las opciones
        for j, op in enumerate(p.opciones):
            print(f"\n    {j+1}. {op['texto']}")
        
        # Leemos la elección del usuario
        try:
            r = int(input("\nTu respuesta (1-4): ")) - 1
            if r < 0 or r >= len(p.opciones):
                raise ValueError
        except ValueError:
            print("\nEntrada no válida. Se contará como incorrecta.")
            fallos += 1
            pausa()
            continue

        # Comprobamos si la respuesta escogida es la correcta
        if p.opciones[r]['correcta']:
            print("\n¡Correcto!")
            aciertos += 1
        else:
            correcta = next(op for op in p.opciones if op['correcta'])
            print(f"\nIncorrecto.\n\nLa respuesta correcta es:\n{correcta['texto']}")
            fallos += 1
        pausa()
    
    # Calculamos los resultados y los mostramos
    limpiar_pantalla()
    fin = datetime.datetime.now()
    duracion = fin - inicio
    nota = round((aciertos - (fallos / 3)) / len(preguntas), 2) * 10
    
    print(f"\nAciertos: {aciertos}.\nFallos: {fallos}.\nNota final: {nota}.\nTiempo: {duracion}")
    
    # Guardamos el examen
    guardar_examen(preguntas, aciertos, fallos, nota, inicio, duracion)
