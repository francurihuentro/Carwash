import json
import os
from pathlib import Path


class RepositorioJSON:
    def __init__(self, ruta):
        self.ruta = Path(ruta)

    def cargar(self):
        if not self.ruta.exists():
            return None
        try:
            with self.ruta.open("r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except (OSError, json.JSONDecodeError) as error:
            raise ValueError("No se pudo leer el archivo de datos de CarWash.") from error

    def guardar(self, datos):
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        temporal = self.ruta.with_suffix(self.ruta.suffix + ".tmp")
        try:
            with temporal.open("w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=2)
            os.replace(temporal, self.ruta)
        finally:
            temporal.unlink(missing_ok=True)
