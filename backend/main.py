import os

from gestor_preguntas import agregar_pregunta
from examen import hacer_examen
from utilidades import pausa

def pintar_menu():
    print("\n--- MENÚ ---")
    print("\n1. Añadir pregunta.")
    print("\n2. Hacer examen.")
    print("\n3. Salir.")
    

def limpiar_pantalla():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def main():
    while True:
        limpiar_pantalla()
        pintar_menu()
        
        opcion = input("\nElige una opción: ")   
        match opcion:
            case "1":    
                limpiar_pantalla()
                agregar_pregunta()
                pausa()
            case "2":
                tema = int(input("Tema del examen: "))
                limpiar_pantalla()
                hacer_examen(tema)
                pausa()
            case "3":
                limpiar_pantalla()
                print("\nHasta la próxima.")
                break
            case _:
                print("\nOpción incorrecta.")
                pausa()
                
if True:
    main()