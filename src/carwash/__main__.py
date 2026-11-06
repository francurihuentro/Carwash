from pathlib import Path
from tkinter import messagebox

from carwash.controladores.controlador import ControladorCarWash
from carwash.modelo.sistema import SistemaCarWash
from carwash.persistencia.repositorio_json import RepositorioJSON
from carwash.vista.aplicacion import AplicacionCarWash


def main():
    ruta_proyecto = Path(__file__).resolve().parents[2]
    ruta_datos = ruta_proyecto / "data" / "carwash.json"
    try:
        sistema = SistemaCarWash(RepositorioJSON(ruta_datos))
    except (OSError, ValueError) as error:
        messagebox.showerror("CarWash: error al iniciar", str(error))
        return
    aplicacion = AplicacionCarWash(ControladorCarWash(sistema))
    aplicacion.mainloop()


if __name__ == "__main__":
    main()
