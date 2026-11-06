from tkinter import messagebox, ttk


def pesos(valor):
    return f"$ {valor:,}".replace(",", ".")


def entrada(padre, fila, texto, ancho=26):
    ttk.Label(padre, text=texto).grid(row=fila, column=0, sticky="w", pady=5)
    campo = ttk.Entry(padre, width=ancho)
    campo.grid(row=fila, column=1, sticky="ew", padx=(12, 4), pady=5)
    return campo


def tabla(padre, columnas, anchos):
    contenedor = ttk.Frame(padre)
    contenedor.pack(fill="both", expand=True)
    lista = ttk.Treeview(contenedor, columns=columnas, show="headings", selectmode="browse")
    for columna, ancho in zip(columnas, anchos):
        lista.heading(columna, text=columna)
        lista.column(columna, width=ancho, minwidth=70, anchor="w")
    scroll_y = ttk.Scrollbar(contenedor, orient="vertical", command=lista.yview)
    scroll_x = ttk.Scrollbar(contenedor, orient="horizontal", command=lista.xview)
    lista.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    lista.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")
    contenedor.rowconfigure(0, weight=1)
    contenedor.columnconfigure(0, weight=1)
    return lista


def mostrar_error(pantalla, error):
    messagebox.showerror("CarWash", str(error), parent=pantalla)


class Pantalla(ttk.Frame):
    def __init__(self, master, controlador, actualizar_todo=None):
        super().__init__(master, padding=18)
        self.controlador = controlador
        self.actualizar_todo = actualizar_todo
