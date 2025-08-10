class Pregunta:
    def __init__(self, id, enunciado, opciones):
        self.id = id
        self.enunciado = enunciado
        self.opciones = opciones
        
    def to_dict(self):
        return{
            "id": self.id,
            "enunciado": self.enunciado,
            "opciones": self.opciones,
        }
        
    def from_dict(data):
        return Pregunta(
            id=data["id"],
            enunciado=data["enunciado"],
            opciones=data["opciones"],
        )