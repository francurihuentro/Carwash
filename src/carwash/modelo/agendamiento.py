from dataclasses import dataclass
from enum import Enum


class EstadoAgendamiento(str, Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADO = "Confirmado"
    EN_PROCESO = "En proceso"
    FINALIZADO = "Finalizado"
    CANCELADO = "Cancelado"


@dataclass
class Agendamiento:
    numero: str
    codigo_cliente: str
    codigo_servicio: str
    fecha: str
    hora_inicio: str
    hora_termino: str
    precio_total: int
    estado: EstadoAgendamiento = EstadoAgendamiento.PENDIENTE
