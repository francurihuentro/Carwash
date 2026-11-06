from datetime import date, datetime, time, timedelta
import re

from .agendamiento import Agendamiento, EstadoAgendamiento
from .cliente import Cliente
from .servicio import Servicio, ServicioPremium
from .vehiculo import Vehiculo


APERTURA = time(9, 0)
CIERRE = time(18, 0)


class SistemaCarWash:
    def __init__(self, repositorio=None):
        self.repositorio = repositorio
        self.clientes = {}
        self.servicios = {}
        self.agendamientos = {}
        self.secuencias = {"cliente": 0, "servicio": 0, "agendamiento": 0}

        datos = repositorio.cargar() if repositorio else None
        if datos is None:
            self._crear_servicios_iniciales()
            self._guardar()
        else:
            self._restaurar(datos)

    def _nuevo_codigo(self, tipo, prefijo):
        self.secuencias[tipo] += 1
        return f"{prefijo}-{self.secuencias[tipo]:03d}"

    def _crear_servicios_iniciales(self):
        self.agregar_servicio("Lavado simple", "Lavado exterior", 30, 10000)
        self.agregar_servicio("Lavado full", "Exterior e interior", 60, 15000)
        self.agregar_servicio(
            "Lavado premium", "Lavado completo y terminación premium", 90, 20000, 5000
        )
        self.agregar_servicio("Lavado de motor", "Limpieza de motor", 45, 18000)

    def registrar_cliente(self, nombre, rut, correo, telefono, patente, marca, modelo):
        nombre = nombre.strip()
        rut = rut.replace(".", "").replace(" ", "").upper()
        correo = correo.strip()
        telefono = telefono.strip()
        patente = patente.replace(" ", "").upper()
        marca = marca.strip()
        modelo = modelo.strip()

        if not all((nombre, rut, correo, telefono, patente, marca, modelo)):
            raise ValueError("Completa todos los datos del cliente y su vehículo.")
        if not re.fullmatch(r"\d{7,8}-[\dK]", rut):
            raise ValueError("Escribe el RUT con formato 12345678-9.")
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo):
            raise ValueError("Escribe un correo válido.")
        if any(cliente.rut == rut for cliente in self.clientes.values()):
            raise ValueError("Ya existe un cliente con ese RUT.")
        if any(cliente.vehiculo.patente == patente for cliente in self.clientes.values()):
            raise ValueError("Ya existe un vehículo con esa patente.")

        codigo = self._nuevo_codigo("cliente", "CLI")
        cliente = Cliente(codigo, nombre, rut, correo, telefono, Vehiculo(patente, marca, modelo))
        self.clientes[codigo] = cliente
        self._guardar()
        return cliente

    def agregar_servicio(self, nombre, descripcion, duracion, valor_base, recargo=0):
        nombre, descripcion = nombre.strip(), descripcion.strip()
        if not nombre or not descripcion:
            raise ValueError("Indica nombre y descripción del servicio.")
        try:
            duracion, valor_base, recargo = int(duracion), int(valor_base), int(recargo)
        except (ValueError, TypeError) as error:
            raise ValueError("Duración y valores deben ser números enteros.") from error
        if duracion <= 0 or valor_base < 0 or recargo < 0:
            raise ValueError("La duración debe ser positiva y los valores no negativos.")

        codigo = self._nuevo_codigo("servicio", "SER")
        if recargo:
            servicio = ServicioPremium(codigo, nombre, descripcion, duracion, valor_base, recargo)
        else:
            servicio = Servicio(codigo, nombre, descripcion, duracion, valor_base)
        self.servicios[codigo] = servicio
        self._guardar()
        return servicio

    def _intervalo(self, fecha_texto, hora_texto, minutos):
        try:
            fecha_obj = date.fromisoformat(fecha_texto.strip())
            hora_obj = time.fromisoformat(hora_texto.strip())
        except ValueError as error:
            raise ValueError("Usa fecha AAAA-MM-DD y hora HH:MM.") from error
        inicio = datetime.combine(fecha_obj, hora_obj)
        fin = inicio + timedelta(minutes=minutos)
        if hora_obj < APERTURA or fin.date() != fecha_obj or fin.time() > CIERRE:
            raise ValueError("El servicio debe realizarse completo entre 09:00 y 18:00.")
        return inicio, fin

    def _verificar_disponibilidad(self, inicio, fin, excluir_numero=None):
        for cita in self.agendamientos.values():
            if cita.numero == excluir_numero or cita.estado == EstadoAgendamiento.CANCELADO:
                continue
            cita_inicio = datetime.fromisoformat(f"{cita.fecha}T{cita.hora_inicio}")
            cita_fin = datetime.fromisoformat(f"{cita.fecha}T{cita.hora_termino}")
            if inicio < cita_fin and fin > cita_inicio:
                raise ValueError(f"Ese horario se cruza con el agendamiento {cita.numero}.")

    def horarios_libres(self, fecha_texto, codigo_servicio):
        if codigo_servicio not in self.servicios:
            raise ValueError("Selecciona un servicio válido.")
        servicio = self.servicios[codigo_servicio]
        try:
            fecha_obj = date.fromisoformat(fecha_texto.strip())
        except ValueError as error:
            raise ValueError("Usa una fecha con formato AAAA-MM-DD.") from error
        if fecha_obj < date.today():
            raise ValueError("No puedes agendar en una fecha pasada.")

        opciones = []
        hora = datetime.combine(fecha_obj, APERTURA)
        limite = datetime.combine(fecha_obj, CIERRE)
        while hora + timedelta(minutes=servicio.duracion_minutos) <= limite:
            fin = hora + timedelta(minutes=servicio.duracion_minutos)
            try:
                self._verificar_disponibilidad(hora, fin)
            except ValueError:
                pass
            else:
                if hora > datetime.now():
                    opciones.append(hora.strftime("%H:%M"))
            hora += timedelta(minutes=30)
        return opciones

    def crear_agendamiento(self, codigo_cliente, codigo_servicio, fecha, hora_inicio):
        if codigo_cliente not in self.clientes:
            raise ValueError("Selecciona un cliente registrado.")
        if codigo_servicio not in self.servicios:
            raise ValueError("Selecciona un servicio válido.")
        servicio = self.servicios[codigo_servicio]
        inicio, fin = self._intervalo(fecha, hora_inicio, servicio.duracion_minutos)
        if inicio <= datetime.now():
            raise ValueError("La cita debe comenzar en el futuro.")
        self._verificar_disponibilidad(inicio, fin)

        numero = self._nuevo_codigo("agendamiento", "AGE")
        cita = Agendamiento(
            numero,
            codigo_cliente,
            codigo_servicio,
            inicio.date().isoformat(),
            inicio.strftime("%H:%M"),
            fin.strftime("%H:%M"),
            servicio.calcular_precio(),
        )
        self.agendamientos[numero] = cita
        self._guardar()
        return cita

    def reprogramar_agendamiento(self, numero, fecha, hora_inicio):
        cita = self._obtener_cita(numero)
        if cita.estado not in (EstadoAgendamiento.PENDIENTE, EstadoAgendamiento.CONFIRMADO):
            raise ValueError("Solo se puede reprogramar una cita pendiente o confirmada.")
        minutos = self.servicios[cita.codigo_servicio].duracion_minutos
        inicio, fin = self._intervalo(fecha, hora_inicio, minutos)
        if inicio <= datetime.now():
            raise ValueError("La nueva cita debe comenzar en el futuro.")
        self._verificar_disponibilidad(inicio, fin, excluir_numero=numero)
        cita.fecha = inicio.date().isoformat()
        cita.hora_inicio = inicio.strftime("%H:%M")
        cita.hora_termino = fin.strftime("%H:%M")
        cita.estado = EstadoAgendamiento.PENDIENTE
        self._guardar()
        return cita

    def cambiar_estado(self, numero, nuevo_estado):
        cita = self._obtener_cita(numero)
        nuevo_estado = EstadoAgendamiento(nuevo_estado)
        permitidos = {
            EstadoAgendamiento.PENDIENTE: {EstadoAgendamiento.CONFIRMADO, EstadoAgendamiento.CANCELADO},
            EstadoAgendamiento.CONFIRMADO: {EstadoAgendamiento.EN_PROCESO, EstadoAgendamiento.CANCELADO},
            EstadoAgendamiento.EN_PROCESO: {EstadoAgendamiento.FINALIZADO},
            EstadoAgendamiento.FINALIZADO: set(),
            EstadoAgendamiento.CANCELADO: set(),
        }
        if nuevo_estado not in permitidos[cita.estado]:
            raise ValueError(f"No se puede pasar de {cita.estado.value} a {nuevo_estado.value}.")
        cita.estado = nuevo_estado
        self._guardar()
        return cita

    def _obtener_cita(self, numero):
        try:
            return self.agendamientos[numero]
        except KeyError as error:
            raise ValueError("Selecciona un agendamiento válido.") from error

    def _guardar(self):
        if not self.repositorio:
            return
        datos = {
            "secuencias": self.secuencias,
            "clientes": [
                {
                    "codigo": c.codigo,
                    "nombre": c.nombre,
                    "rut": c.rut,
                    "correo": c.correo,
                    "telefono": c.telefono,
                    "vehiculo": vars(c.vehiculo),
                }
                for c in self.clientes.values()
            ],
            "servicios": [
                {
                    "codigo": s.codigo,
                    "nombre": s.nombre,
                    "descripcion": s.descripcion,
                    "duracion_minutos": s.duracion_minutos,
                    "valor_base": s.valor_base,
                    "recargo_premium": s.recargo_premium if isinstance(s, ServicioPremium) else 0,
                }
                for s in self.servicios.values()
            ],
            "agendamientos": [
                {**vars(a), "estado": a.estado.value} for a in self.agendamientos.values()
            ],
        }
        self.repositorio.guardar(datos)

    def _restaurar(self, datos):
        try:
            self.secuencias = dict(datos["secuencias"])
            for registro in datos["clientes"]:
                vehiculo = Vehiculo(**registro["vehiculo"])
                cliente = Cliente(
                    registro["codigo"], registro["nombre"], registro["rut"],
                    registro["correo"], registro["telefono"], vehiculo
                )
                self.clientes[cliente.codigo] = cliente
            for registro in datos["servicios"]:
                campos = (
                    registro["codigo"], registro["nombre"], registro["descripcion"],
                    registro["duracion_minutos"], registro["valor_base"]
                )
                recargo = registro.get("recargo_premium", 0)
                servicio = ServicioPremium(*campos, recargo) if recargo else Servicio(*campos)
                self.servicios[servicio.codigo] = servicio
            for registro in datos["agendamientos"]:
                registro = dict(registro)
                registro["estado"] = EstadoAgendamiento(registro["estado"])
                cita = Agendamiento(**registro)
                self.agendamientos[cita.numero] = cita
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("El archivo de datos de CarWash está dañado o incompleto.") from error
