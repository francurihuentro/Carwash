import tkinter as tk
from tkinter import messagebox, ttk

from .comun import Pantalla, entrada, mostrar_error, pesos, tabla


class Servicios(Pantalla):
    def __init__(self, master, controlador, actualizar_todo):
        super().__init__(master, controlador, actualizar_todo)
        ttk.Label(self, text="Catálogo de servicios", style="Seccion.TLabel").pack(
            anchor="w", pady=(0, 8)
        )
        formulario = ttk.Frame(self)
        formulario.pack(fill="x", pady=(0, 14))
        formulario.columnconfigure(1, weight=1)
        self.nombre = entrada(formulario, 0, "Nombre")
        self.descripcion = entrada(formulario, 1, "Descripción")
        self.duracion = entrada(formulario, 2, "Duración en minutos")
        self.valor = entrada(formulario, 3, "Valor base en pesos")
        self.recargo = entrada(formulario, 4, "Recargo premium")
        self.recargo.insert(0, "0")
        ttk.Label(
            formulario,
            text="Si el recargo es 0, el servicio es normal; si es mayor, será premium.",
            style="Subtitulo.TLabel",
        ).grid(row=5, column=0, columnspan=2, sticky="w", pady=6)
        ttk.Button(formulario, text="Agregar servicio", command=self.guardar).grid(
            row=6, column=0, columnspan=2, sticky="w", pady=(8, 0)
        )
        self.tabla = tabla(
            self,
            ("Código", "Servicio", "Tipo", "Duración", "Base", "Recargo", "Total", "Descripción"),
            (85, 170, 85, 90, 90, 90, 90, 280),
        )

    def guardar(self):
        try:
            servicio = self.controlador.agregar_servicio(
                self.nombre.get(), self.descripcion.get(), self.duracion.get(),
                self.valor.get(), self.recargo.get()
            )
        except (ValueError, OSError) as error:
            mostrar_error(self, error)
            return
        for campo in (self.nombre, self.descripcion, self.duracion, self.valor, self.recargo):
            campo.delete(0, tk.END)
        self.recargo.insert(0, "0")
        self.actualizar_todo()
        messagebox.showinfo("Servicio guardado", f"Se agregó {servicio.nombre}.", parent=self)

    def refrescar(self):
        self.tabla.delete(*self.tabla.get_children())
        for servicio in self.controlador.servicios():
            recargo = getattr(servicio, "recargo_premium", 0)
            self.tabla.insert(
                "", "end", iid=servicio.codigo,
                values=(
                    servicio.codigo, servicio.nombre, servicio.tipo,
                    f"{servicio.duracion_minutos} min", pesos(servicio.valor_base),
                    pesos(recargo), pesos(servicio.calcular_precio()), servicio.descripcion
                ),
            )
