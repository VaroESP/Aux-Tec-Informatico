import os

def pausa():
    input("\nPresione 'ENTER' para continuar...")
    
def limpiar_pantalla():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")