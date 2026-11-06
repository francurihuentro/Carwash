from datetime import date, timedelta
import tkinter as tk
from tkinter import messagebox, ttk

from .comun import Pantalla, mostrar_error, pesos, tabla


class Agenda(Pantalla):
    def __init__(self, master, controlador, actualizar_todo):
        super().__init__(master, controlador, actualizar_todo)
        self.opciones_clientes = {}
        self.opciones_servicios = {}

        ttk.Label(self, text="Crear y gestionar citas", style="Seccion.TLabel").pack(
            anchor="w", pady=(0, 8)
        )
        formulario = ttk.Frame(self)
        formulario.pack(fill="x", pady=(0, 8))
        formulario.columnconfigure(1, weight=1)
        formulario.columnconfigure(3, weight=1)
        ttk.Label(formulario, text="Cliente").grid(row=0, column=0, sticky="w", pady=5)
        self.combo_cliente = ttk.Combobox(formulario, state="readonly")
        self.combo_cliente.grid(row=0, column=1, sticky="ew", padx=(10, 24), pady=5)
        ttk.Label(formulario, text="Servicio").grid(row=0, column=2, sticky="w", pady=5)
        self.combo_servicio = ttk.Combobox(formulario, state="readonly")
        self.combo_servicio.grid(row=0, column=3, sticky="ew", padx=(10, 4), pady=5)
        ttk.Label(formulario, text="Fecha (AAAA-MM-DD)").grid(row=1, column=0, sticky="w", pady=5)
        self.fecha = ttk.Entry(formulario)
        self.fecha.insert(0, (date.today() + timedelta(days=1)).isoformat())
        self.fecha.grid(row=1, column=1, sticky="ew", padx=(10, 24), pady=5)
        ttk.Label(formulario, text="Hora (HH:MM)").grid(row=1, column=2, sticky="w", pady=5)
        self.hora = ttk.Combobox(formulario)
        self.hora.grid(row=1, column=3, sticky="ew", padx=(10, 4), pady=5)

        botones = ttk.Frame(self)
        botones.pack(fill="x", pady=(0, 12))
        ttk.Button(botones, text="Ver horarios libres", command=self.ver_horarios).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(botones, text="Crear cita", command=self.crear_cita).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(botones, text="Reprogramar seleccionada", command=self.reprogramar).pack(
            side="left"
        )
        ttk.Label(self, text="Agendamientos", style="Seccion.TLabel").pack(
            anchor="w", pady=(2, 8)
        )
        self.tabla = tabla(
            self,
            ("Número", "Fecha", "Inicio", "Término", "Cliente", "Patente", "Servicio", "Total", "Estado"),
            (90, 100, 70, 70, 150, 90, 160, 90, 100),
        )
        self.tabla.bind("<<TreeviewSelect>>", self.cita_seleccionada)

        acciones = ttk.Frame(self)
        acciones.pack(fill="x", pady=(10, 0))
        ttk.Button(acciones, text="Confirmar", command=lambda: self.cambiar_estado("confirmar")).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(acciones, text="Iniciar lavado", command=lambda: self.cambiar_estado("iniciar")).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(acciones, text="Finalizar", command=lambda: self.cambiar_estado("finalizar")).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(acciones, text="Cancelar", command=lambda: self.cambiar_estado("cancelar")).pack(
            side="left"
        )

    def codigo_cliente(self):
        try:
            return self.opciones_clientes[self.combo_cliente.get()]
        except KeyError as error:
            raise ValueError("Selecciona un cliente.") from error

    def codigo_servicio(self):
        try:
            return self.opciones_servicios[self.combo_servicio.get()]
        except KeyError as error:
            raise ValueError("Selecciona un servicio.") from error

    def ver_horarios(self):
        try:
            opciones = self.controlador.horarios_libres(
                self.fecha.get(), self.codigo_servicio()
            )
        except ValueError as error:
            mostrar_error(self, error)
            return
        self.hora["values"] = opciones
        if opciones:
            self.hora.set(opciones[0])
            messagebox.showinfo(
                "Horarios libres", "Opciones disponibles:\n" + ", ".join(opciones), parent=self
            )
        else:
            self.hora.set("")
            messagebox.showinfo("Horarios libres", "No hay horarios disponibles.", parent=self)

    def crear_cita(self):
        try:
            cita = self.controlador.crear_agendamiento(
                self.codigo_cliente(), self.codigo_servicio(),
                self.fecha.get(), self.hora.get()
            )
        except (ValueError, OSError) as error:
            mostrar_error(self, error)
            return
        self.actualizar_todo()
        self.tabla.selection_set(cita.numero)
        self.tabla.see(cita.numero)
        messagebox.showinfo(
            "Cita creada",
            f"{cita.numero}: {cita.fecha} de {cita.hora_inicio} a {cita.hora_termino}.\n"
            f"Total: {pesos(cita.precio_total)}.",
            parent=self,
        )

    def numero_seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            raise ValueError("Selecciona una cita en la tabla.")
        return seleccion[0]

    def reprogramar(self):
        try:
            cita = self.controlador.reprogramar(
                self.numero_seleccionado(), self.fecha.get(), self.hora.get()
            )
        except (ValueError, OSError) as error:
            mostrar_error(self, error)
            return
        self.actualizar_todo()
        self.tabla.selection_set(cita.numero)
        self.tabla.see(cita.numero)
        messagebox.showinfo(
            "Cita reprogramada",
            f"{cita.numero} quedó para {cita.fecha} a las {cita.hora_inicio}.\n"
            "Volvió a Pendiente para que se confirme nuevamente.",
            parent=self,
        )

    def cambiar_estado(self, accion):
        try:
            numero = self.numero_seleccionado()
            if accion == "cancelar" and not messagebox.askyesno(
                "Cancelar cita", f"¿Cancelar el agendamiento {numero}?", parent=self
            ):
                return
            cita = getattr(self.controlador, accion)(numero)
        except (ValueError, OSError) as error:
            mostrar_error(self, error)
            return
        self.actualizar_todo()
        self.tabla.selection_set(cita.numero)
        self.tabla.see(cita.numero)

    def cita_seleccionada(self, _evento):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        cita = self.controlador.sistema.agendamientos[seleccion[0]]
        self.fecha.delete(0, tk.END)
        self.fecha.insert(0, cita.fecha)
        self.hora.set(cita.hora_inicio)
        for texto, codigo in self.opciones_clientes.items():
            if codigo == cita.codigo_cliente:
                self.combo_cliente.set(texto)
                break
        for texto, codigo in self.opciones_servicios.items():
            if codigo == cita.codigo_servicio:
                self.combo_servicio.set(texto)
                break

    def refrescar(self):
        clientes = self.controlador.clientes()
        servicios = self.controlador.servicios()
        citas = self.controlador.agendamientos()

        self.opciones_clientes = {
            f"{c.codigo} · {c.nombre} ({c.vehiculo.patente})": c.codigo for c in clientes
        }
        self.opciones_servicios = {
            f"{s.codigo} · {s.nombre} ({pesos(s.calcular_precio())})": s.codigo
            for s in servicios
        }
        cliente_actual = self.combo_cliente.get()
        servicio_actual = self.combo_servicio.get()
        self.combo_cliente["values"] = list(self.opciones_clientes)
        self.combo_servicio["values"] = list(self.opciones_servicios)
        if cliente_actual not in self.opciones_clientes:
            self.combo_cliente.set(next(iter(self.opciones_clientes), ""))
        if servicio_actual not in self.opciones_servicios:
            self.combo_servicio.set(next(iter(self.opciones_servicios), ""))

        self.tabla.delete(*self.tabla.get_children())
        for cita in citas:
            cliente = self.controlador.cliente(cita.codigo_cliente)
            servicio = self.controlador.servicio(cita.codigo_servicio)
            self.tabla.insert(
                "", "end", iid=cita.numero,
                values=(
                    cita.numero, cita.fecha, cita.hora_inicio, cita.hora_termino,
                    cliente.nombre, cliente.vehiculo.patente, servicio.nombre,
                    pesos(cita.precio_total), cita.estado.value
                ),
            )
