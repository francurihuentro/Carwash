import tkinter as tk
from tkinter import ttk

from .agenda import Agenda
from .clientes import Clientes
from .inicio import Inicio
from .servicios import Servicios


class AplicacionCarWash(tk.Tk):
    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador
        self.title("CarWash · Sistema de agendamientos")
        self.geometry("1160x760")
        self.minsize(920, 650)
        self.configure(bg="#eef3f7")
        self._configurar_estilo()

        encabezado = ttk.Frame(self, padding=(20, 16))
        encabezado.pack(fill="x")
        ttk.Label(encabezado, text="CarWash", style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(
            encabezado,
            text="Agenda de servicios de lavado · Versión alfa 0.1",
            style="Subtitulo.TLabel",
        ).pack(anchor="w")

        self.pestanas = ttk.Notebook(self)
        self.pestanas.pack(fill="both", expand=True, padx=20, pady=(0, 18))
        self.inicio = Inicio(self.pestanas, controlador)
        self.clientes = Clientes(self.pestanas, controlador, self.actualizar_todo)
        self.servicios = Servicios(self.pestanas, controlador, self.actualizar_todo)
        self.agenda = Agenda(self.pestanas, controlador, self.actualizar_todo)
        for pantalla, nombre in (
            (self.inicio, "Inicio"),
            (self.clientes, "Clientes"),
            (self.servicios, "Servicios"),
            (self.agenda, "Agenda"),
        ):
            self.pestanas.add(pantalla, text=f"  {nombre}  ")
        self.actualizar_todo()

    def _configurar_estilo(self):
        estilo = ttk.Style(self)
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")
        estilo.configure(".", font=("Segoe UI", 10))
        estilo.configure("TFrame", background="#eef3f7")
        estilo.configure("TLabel", background="#eef3f7", foreground="#1d3142")
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 22, "bold"))
        estilo.configure("Subtitulo.TLabel", foreground="#597080")
        estilo.configure("Seccion.TLabel", font=("Segoe UI", 13, "bold"))
        estilo.configure("TButton", padding=(10, 6))
        estilo.configure("Treeview", rowheight=28, background="white")
        estilo.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        estilo.configure("TNotebook", background="#eef3f7", borderwidth=0)
        estilo.configure("TNotebook.Tab", padding=(14, 8))

    def actualizar_todo(self):
        for pantalla in (self.inicio, self.clientes, self.servicios, self.agenda):
            pantalla.refrescar()
