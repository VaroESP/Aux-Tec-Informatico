class Pregunta:
    def __init__(self, id, enunciado, opciones, respuesta_correcta, tema):
        self.id = id
        self.enunciado = enunciado
        self.opciones = opciones
        self.respuesta_correcta = respuesta_correcta
        self.tema = tema
        
    def to_dict(self):
        return{
            "id": self.id,
            "enunciado": self.enunciado,
            "opciones": self.opciones,
            "respuesta_correcta": self.respuesta_correcta,
            "tema": self.tema
        }
        
    def from_dict(data):
        return Pregunta(
            id=data["id"],
            enunciado=data["enunciado"],
            opciones=data["opciones"],
            respuesta_correcta=data["respuesta_correcta"],
            tema=data["tema"]
        )