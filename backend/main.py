import os

from gestor_examenes import nuevo_examen, listar_examenes
from gestor_preguntas import agregar_pregunta
from utilidades import pausa, limpiar_pantalla

def pintar_menu():
    print("\n--- MENÚ ---")
    print("\n1. Hacer examen.")
    print("\n2. Añadir preguntas.")
    print("\n3. Listado de exámenes.")
    print("\n4. Salir.")

def main():
    while True:
        limpiar_pantalla()
        pintar_menu()
        
        opcion = input("\nElige una opción: ")   
        match opcion:
            case "1":
                limpiar_pantalla()
                nuevo_examen()
                pausa()
            case "2":
                limpiar_pantalla()
                agregar_pregunta()
                pausa()
            case "3":
                limpiar_pantalla()
                listar_examenes()
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