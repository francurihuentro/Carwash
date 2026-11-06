from dataclasses import dataclass

from .vehiculo import Vehiculo


@dataclass
class Cliente:
    codigo: str
    nombre: str
    rut: str
    correo: str
    telefono: str
    vehiculo: Vehiculo
