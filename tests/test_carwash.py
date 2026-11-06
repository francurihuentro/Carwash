from datetime import date, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from carwash.modelo.agendamiento import EstadoAgendamiento
from carwash.modelo.servicio import ServicioPremium
from carwash.modelo.sistema import SistemaCarWash
from carwash.persistencia.repositorio_json import RepositorioJSON


class PruebasCarWash(unittest.TestCase):
    def setUp(self):
        self.sistema = SistemaCarWash()
        self.fecha = (date.today() + timedelta(days=1)).isoformat()
        self.cliente = self.sistema.registrar_cliente(
            "Ana Pérez", "12345678-9", "ana@ejemplo.cl",
            "912345678", "ABCD12", "Toyota", "Yaris"
        )
        self.normal = next(
            s for s in self.sistema.servicios.values() if s.nombre == "Lavado full"
        )
        self.premium = next(
            s for s in self.sistema.servicios.values() if isinstance(s, ServicioPremium)
        )

    def test_herencia_y_precio_polimorfico(self):
        self.assertEqual(self.normal.calcular_precio(), 15000)
        self.assertEqual(self.premium.calcular_precio(), 25000)
        cita = self.sistema.crear_agendamiento(
            self.cliente.codigo, self.premium.codigo, self.fecha, "09:00"
        )
        self.assertEqual(cita.precio_total, 25000)
        self.assertEqual(cita.hora_termino, "10:30")

    def test_impide_horarios_superpuestos(self):
        self.sistema.crear_agendamiento(
            self.cliente.codigo, self.normal.codigo, self.fecha, "09:00"
        )
        with self.assertRaisesRegex(ValueError, "se cruza"):
            self.sistema.crear_agendamiento(
                self.cliente.codigo, self.normal.codigo, self.fecha, "09:30"
            )
        self.sistema.crear_agendamiento(
            self.cliente.codigo, self.normal.codigo, self.fecha, "10:00"
        )

    def test_cancelar_libera_horario(self):
        cita = self.sistema.crear_agendamiento(
            self.cliente.codigo, self.normal.codigo, self.fecha, "09:00"
        )
        self.sistema.cambiar_estado(cita.numero, EstadoAgendamiento.CANCELADO)
        nueva = self.sistema.crear_agendamiento(
            self.cliente.codigo, self.normal.codigo, self.fecha, "09:00"
        )
        self.assertNotEqual(cita.numero, nueva.numero)

    def test_transiciones_y_reprogramacion(self):
        cita = self.sistema.crear_agendamiento(
            self.cliente.codigo, self.normal.codigo, self.fecha, "09:00"
        )
        self.sistema.cambiar_estado(cita.numero, EstadoAgendamiento.CONFIRMADO)
        self.sistema.reprogramar_agendamiento(cita.numero, self.fecha, "10:00")
        self.assertEqual(cita.estado, EstadoAgendamiento.PENDIENTE)
        self.sistema.cambiar_estado(cita.numero, EstadoAgendamiento.CONFIRMADO)
        self.sistema.cambiar_estado(cita.numero, EstadoAgendamiento.EN_PROCESO)
        self.sistema.cambiar_estado(cita.numero, EstadoAgendamiento.FINALIZADO)
        with self.assertRaisesRegex(ValueError, "No se puede"):
            self.sistema.cambiar_estado(cita.numero, EstadoAgendamiento.CANCELADO)

    def test_datos_persisten_en_json(self):
        with TemporaryDirectory(dir=Path.cwd()) as carpeta:
            repositorio = RepositorioJSON(Path(carpeta) / "carwash.json")
            sistema = SistemaCarWash(repositorio)
            cliente = sistema.registrar_cliente(
                "Luis Soto", "87654321-K", "luis@ejemplo.cl",
                "987654321", "EFGH34", "Kia", "Rio"
            )
            servicio = next(iter(sistema.servicios.values()))
            cita = sistema.crear_agendamiento(
                cliente.codigo, servicio.codigo, self.fecha, "11:00"
            )
            recargado = SistemaCarWash(repositorio)
            self.assertIn(cliente.codigo, recargado.clientes)
            self.assertIn(cita.numero, recargado.agendamientos)
            self.assertEqual(
                recargado.agendamientos[cita.numero].precio_total, servicio.calcular_precio()
            )


if __name__ == "__main__":
    unittest.main()
