from datetime import datetime, timedelta
from pregunta import Pregunta

class Examen:
    def __init__(self, id, preguntas, aciertos, fallos, nota, inicio, duracion):
        self.id = id
        self.preguntas = preguntas
        self.aciertos = aciertos
        self.fallos = fallos
        self.nota = nota
        self.inicio = inicio
        self.duracion = duracion
    
    def to_dict(self):
        return{
            "id": self.id,
            "preguntas": [p.to_dict() for p in self.preguntas],
            "aciertos": self.aciertos,
            "fallos": self.fallos,
            "nota": self.nota,
            "inicio": self.inicio.isoformat() if self.inicio else None,
            "duracion": self.duracion.total_seconds() if isinstance(self.duracion, timedelta) else self.duracion
    }
    
    @staticmethod    
    def from_dict(data):
        preguntas = [Pregunta.from_dict(p) for p in data.get("preguntas", [])]
        inicio = datetime.fromisoformat(data["inicio"]) if data.get("inicio") else None
        duracion_val = data.get("duracion")
        duracion = timedelta(seconds=duracion_val) if duracion_val is not None else None
        
        return Examen(
            id=data.get("id"),
            preguntas=preguntas,
            aciertos=data.get("aciertos"),
            fallos=data.get("fallos"),
            nota=data.get("nota"),
            inicio=inicio,
            duracion=duracion
        )