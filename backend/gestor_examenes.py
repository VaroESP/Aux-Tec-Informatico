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
            partes.append(f"{horas}h")
        if minutos > 0:
            partes.append(f"{minutos}m")
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
        
def nuevo_examen_tema():
    limpiar_pantalla()
    tema = input("\nIntroduce el número del tema: ")
    
    # Cargamos las preguntas
    preguntas = cargar_preguntas(tema)
    
    preguntas_examen = random.sample(preguntas, 25)
    
    aciertos = 0
    fallos = 0
    
    #Comenzamos el examen  
    inicio = datetime.datetime.now()
    for i, p in enumerate(preguntas_examen):
        limpiar_pantalla()
        
        # Mostramos el enunciado
        print(f"\n{i+1}. {p.enunciado}")
        
        # Mezclamos las opciones
        opciones_mezcladas = p.opciones[:]
        random.shuffle(opciones_mezcladas)
        
        # Mostramos las opciones mezcladas
        for j, op in enumerate(opciones_mezcladas):
            print(f"\n    {j+1}. {op['texto']}")
        
        # Leemos la elección del usuario
        while True:
            try:
                r = int(input("\nTu respuesta (1-4): ")) - 1
                if 0 <= r < len(opciones_mezcladas):
                    # Respuesta correcta. Salimos del bucle
                    break
                else:
                    print("\nNúmero no válido.")
            except ValueError:
                print("\nEntrada no válida.")

        # Comprobamos si la respuesta escogida es la correcta
        if opciones_mezcladas[r]['correcta']:
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
    nota = round((aciertos - (fallos / 3)) / len(preguntas_examen), 2) * 10
    
    print(f"\nAciertos: {aciertos}.\nFallos: {fallos}.\nNota final: {nota}.\nTiempo: {duracion}")
    
    # Guardamos el examen
    guardar_examen(preguntas, aciertos, fallos, nota, inicio, duracion)
          

def nuevo_examen_completo():
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
    
    contador_tema = 1
    for i, p in enumerate(preguntas):
        limpiar_pantalla()
        
        # Mostramos el tema correspondiente a la pregunta
        if contador_tema <= PREGUNTAS_POR_TEMA:
            print("\nTema 1. La Constitución española de 1978.")
        elif contador_tema <= PREGUNTAS_POR_TEMA * 2:
            print("\nTema 2. Estatutos de la universidad (I).")
        elif contador_tema <= PREGUNTAS_POR_TEMA * 3:
            print("\nTema 3. Estatutos de la universidad (II).")
        elif contador_tema <= PREGUNTAS_POR_TEMA * 4:
            print("\nTema 4. Estatutos de la universidad (III).")
        elif contador_tema <= PREGUNTAS_POR_TEMA * 5:
            print("\nTema 5. Ley 39/2015, 1 de octubre. Procedimiento Administrativo Común.")
        elif contador_tema <= PREGUNTAS_POR_TEMA * 6:
            print("\nTema 6. Estatuto básico del empleado público (I).")
        elif contador_tema <= PREGUNTAS_POR_TEMA * 7:
            print("\nTema 7. Estatuto básico del empleado público (II).")
        elif contador_tema <= PREGUNTAS_POR_TEMA * 8:
            print("\nTema 8. Estatuto básico del empleado público (III).")
        elif contador_tema <= PREGUNTAS_POR_TEMA * 9:
            print("\nTema 9. Acuerdo regulador de las condiciones de trabajo de la UEX (I).")
        elif contador_tema <= PREGUNTAS_POR_TEMA * 10:
            print("\nTema 10. Acuerdo regulador de las condiciones de trabajo de la UEX (II).")

        
        
        # Mostramos el enunciado
        print(f"\n{i+1}. {p.enunciado}")
        
        # Mezclamos las opciones
        opciones_mezcladas = p.opciones[:]
        random.shuffle(opciones_mezcladas)
        
        # Mostramos las opciones mezcladas
        for j, op in enumerate(opciones_mezcladas):
            print(f"\n    {j+1}. {op['texto']}")
        
        # Leemos la elección del usuario
        while True:
            try:
                r = int(input("\nTu respuesta (1-4): ")) - 1
                if 0 <= r < len(opciones_mezcladas):
                    # Respuesta correcta. Salimos del bucle
                    break
                else:
                    print("\nNúmero no válido.")
            except ValueError:
                print("\nEntrada no válida.")

        # Comprobamos si la respuesta escogida es la correcta
        if opciones_mezcladas[r]['correcta']:
            print("\n¡Correcto!")
            aciertos += 1
        else:
            correcta = next(op for op in p.opciones if op['correcta'])
            print(f"\nIncorrecto.\n\nLa respuesta correcta es:\n{correcta['texto']}")
            fallos += 1
        
        contador_tema += 1
        pausa()
    
    # Calculamos los resultados y los mostramos
    limpiar_pantalla()
    fin = datetime.datetime.now()
    duracion = fin - inicio
    nota = round((aciertos - (fallos / 3)) / len(preguntas), 2) * 10
    
    print(f"\nAciertos: {aciertos}.\nFallos: {fallos}.\nNota final: {nota}.\nTiempo: {duracion}")
    
    # Guardamos el examen
    guardar_examen(preguntas, aciertos, fallos, nota, inicio, duracion)
