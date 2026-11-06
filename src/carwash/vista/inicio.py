from tkinter import ttk

from .comun import Pantalla


class Inicio(Pantalla):
    def __init__(self, master, controlador):
        super().__init__(master, controlador)
        ttk.Label(self, text="Bienvenido a la agenda", style="Seccion.TLabel").pack(
            anchor="w", pady=(0, 10)
        )
        ttk.Label(
            self,
            text=(
                "1. Registra un cliente y su vehículo.\n"
                "2. Revisa o agrega los servicios.\n"
                "3. Busca un horario libre y crea un agendamiento.\n"
                "4. Selecciona la cita para confirmarla, iniciarla, finalizarla o cancelarla."
            ),
            justify="left",
        ).pack(anchor="w", pady=8)
        self.resumen = ttk.Label(self, text="", style="Seccion.TLabel")
        self.resumen.pack(anchor="w", pady=(24, 8))
        ttk.Label(
            self,
            text=(
                "Atención de 09:00 a 18:00 en un puesto de lavado."
            ),
            wraplength=760,
            style="Subtitulo.TLabel",
        ).pack(anchor="w")

    def refrescar(self):
        self.resumen.configure(
            text=(
                f"{len(self.controlador.clientes())} clientes  ·  "
                f"{len(self.controlador.servicios())} servicios  ·  "
                f"{len(self.controlador.agendamientos())} citas"
            )
        )
