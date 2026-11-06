import tkinter as tk
from tkinter import messagebox, ttk

from .comun import Pantalla, entrada, mostrar_error, tabla


class Clientes(Pantalla):
    def __init__(self, master, controlador, actualizar_todo):
        super().__init__(master, controlador, actualizar_todo)
        ttk.Label(self, text="Registrar cliente y vehículo", style="Seccion.TLabel").pack(
            anchor="w", pady=(0, 8)
        )
        formulario = ttk.Frame(self)
        formulario.pack(fill="x", pady=(0, 14))
        formulario.columnconfigure(1, weight=1)
        formulario.columnconfigure(3, weight=1)
        self.nombre = entrada(formulario, 0, "Nombre")
        self.rut = entrada(formulario, 1, "RUT")
        self.correo = entrada(formulario, 2, "Correo")
        self.telefono = entrada(formulario, 3, "Teléfono")
        for fila, etiqueta in enumerate(("Patente", "Marca", "Modelo")):
            ttk.Label(formulario, text=etiqueta).grid(row=fila, column=2, sticky="w", padx=(24, 0))
        self.patente = ttk.Entry(formulario)
        self.marca = ttk.Entry(formulario)
        self.modelo = ttk.Entry(formulario)
        for fila, campo in enumerate((self.patente, self.marca, self.modelo)):
            campo.grid(row=fila, column=3, sticky="ew", padx=(12, 4), pady=5)
        ttk.Button(formulario, text="Guardar cliente", command=self.guardar).grid(
            row=4, column=0, columnspan=4, sticky="w", pady=(10, 0)
        )
        ttk.Label(self, text="Clientes registrados", style="Seccion.TLabel").pack(
            anchor="w", pady=(4, 8)
        )
        self.tabla = tabla(
            self,
            ("Código", "Nombre", "RUT", "Correo", "Teléfono", "Patente", "Vehículo"),
            (85, 160, 110, 190, 110, 100, 170),
        )

    def guardar(self):
        try:
            cliente = self.controlador.registrar_cliente(
                self.nombre.get(), self.rut.get(), self.correo.get(),
                self.telefono.get(), self.patente.get(), self.marca.get(), self.modelo.get()
            )
        except (ValueError, OSError) as error:
            mostrar_error(self, error)
            return
        for campo in (
            self.nombre, self.rut, self.correo, self.telefono,
            self.patente, self.marca, self.modelo
        ):
            campo.delete(0, tk.END)
        self.actualizar_todo()
        messagebox.showinfo("Cliente guardado", f"Se registró {cliente.nombre}.", parent=self)

    def refrescar(self):
        self.tabla.delete(*self.tabla.get_children())
        for cliente in self.controlador.clientes():
            vehiculo = cliente.vehiculo
            self.tabla.insert(
                "", "end", iid=cliente.codigo,
                values=(
                    cliente.codigo, cliente.nombre, cliente.rut, cliente.correo,
                    cliente.telefono, vehiculo.patente, f"{vehiculo.marca} {vehiculo.modelo}"
                ),
            )
