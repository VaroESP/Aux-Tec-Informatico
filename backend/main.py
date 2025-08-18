import os

from gestor_examenes import nuevo_examen_completo, nuevo_examen_tema, listar_examenes
from gestor_preguntas import agregar_pregunta, importar_preguntas
from utilidades import pausa, limpiar_pantalla

def pintar_menu():
    print("\n--- MENÚ ---")
    print("\n1. Hacer examen.")
    print("\n2. Añadir preguntas.")
    print("\n3. Listado de exámenes.")
    print("\n4. Importar preguntas de archivo.")
    print("\n5. Salir.")

def main():
    while True:
        limpiar_pantalla()
        pintar_menu()
        
        opcion = input("\nElige una opción: ")
        match opcion:
            case "1":
                # Hay que completarlo
                limpiar_pantalla()
                print("\n--- Nuevo Examen ---")
                print("\n1. Examen por tema.")
                print("\n2. Examen completo.")
                opcion = input("\nElige una opción: ")
                if opcion == "1":
                    nuevo_examen_tema()
                elif opcion == "2":
                    nuevo_examen_completo()
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
                importar_preguntas()
                pausa()
            case "5":
                limpiar_pantalla()
                print("\nHasta la próxima.")
                break
            case _:
                print("\nOpción incorrecta.")
                pausa()
                
if True:
    main()