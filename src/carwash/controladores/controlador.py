from carwash.modelo.agendamiento import EstadoAgendamiento


class ControladorCarWash:
    def __init__(self, sistema):
        self.sistema = sistema

    def clientes(self):
        return sorted(self.sistema.clientes.values(), key=lambda c: c.nombre.lower())

    def servicios(self):
        return list(self.sistema.servicios.values())

    def agendamientos(self):
        return sorted(
            self.sistema.agendamientos.values(),
            key=lambda a: (a.fecha, a.hora_inicio, a.numero),
        )

    def cliente(self, codigo):
        return self.sistema.clientes[codigo]

    def servicio(self, codigo):
        return self.sistema.servicios[codigo]

    def registrar_cliente(self, nombre, rut, correo, telefono, patente, marca, modelo):
        return self.sistema.registrar_cliente(
            nombre, rut, correo, telefono, patente, marca, modelo
        )

    def agregar_servicio(self, nombre, descripcion, duracion, valor_base, recargo):
        return self.sistema.agregar_servicio(
            nombre, descripcion, duracion, valor_base, recargo
        )

    def horarios_libres(self, fecha, codigo_servicio):
        return self.sistema.horarios_libres(fecha, codigo_servicio)

    def crear_agendamiento(self, codigo_cliente, codigo_servicio, fecha, hora):
        return self.sistema.crear_agendamiento(
            codigo_cliente, codigo_servicio, fecha, hora
        )

    def reprogramar(self, numero, fecha, hora):
        return self.sistema.reprogramar_agendamiento(numero, fecha, hora)

    def confirmar(self, numero):
        return self.sistema.cambiar_estado(numero, EstadoAgendamiento.CONFIRMADO)

    def iniciar(self, numero):
        return self.sistema.cambiar_estado(numero, EstadoAgendamiento.EN_PROCESO)

    def finalizar(self, numero):
        return self.sistema.cambiar_estado(numero, EstadoAgendamiento.FINALIZADO)

    def cancelar(self, numero):
        return self.sistema.cambiar_estado(numero, EstadoAgendamiento.CANCELADO)
