import os

from gestor_preguntas import agregar_preguntas, importar_preguntas
from examen import hacer_examen
from utilidades import pausa, limpiar_pantalla

def pintar_menu():
    print("\n--- MENÚ ---")
    print("\n1. Añadir pregunta.")
    print("\n2. Añadir preguntas de archivo.")
    print("\n3. Hacer examen.")
    print("\n4. Salir.")

def main():
    while True:
        limpiar_pantalla()
        pintar_menu()
        
        opcion = input("\nElige una opción: ")   
        match opcion:
            case "1":    
                limpiar_pantalla()
                agregar_preguntas()
                pausa()
            case "2":
                limpiar_pantalla()
                importar_preguntas("preguntas_nuevas.json")
                pausa()
            case "3":
                tema = int(input("Tema del examen: "))
                limpiar_pantalla()
                hacer_examen(tema)
                pausa()
            case "4":
                limpiar_pantalla()
                print("\nHasta la próxima.")
                break
            case _:
                print("\nOpción incorrecta.")
                pausa()
                
if True:
    main()