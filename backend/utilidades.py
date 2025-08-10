import os

def pausa():
    input("\nPresione 'ENTER' para continuar...")
    
def limpiar_pantalla():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
        
def num_archivos(ruta):
    archivos = [f for f in os.listdir(ruta) if os.path.isfile(os.path.join(ruta, f))]
    num = len(archivos)
    return num