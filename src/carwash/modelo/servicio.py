from dataclasses import dataclass


@dataclass
class Servicio:
    codigo: str
    nombre: str
    descripcion: str
    duracion_minutos: int
    valor_base: int

    def calcular_precio(self) -> int:
        return self.valor_base

    @property
    def tipo(self) -> str:
        return "Normal"


@dataclass
class ServicioPremium(Servicio):
    recargo_premium: int

    def calcular_precio(self) -> int:
        return self.valor_base + self.recargo_premium

    @property
    def tipo(self) -> str:
        return "Premium"
