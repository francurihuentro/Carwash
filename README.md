# CarWash — versión alfa 0.1

Aplicación de escritorio para registrar clientes y gestionar agendamientos de lavado.
Organiza el código en modelo, vista, controlador y persistencia JSON, siguiendo la
estructura del proyecto FlashFood usado como referencia.

## Cómo abrirlo

1. Instala Python 3.10 o posterior con Tkinter.
2. Abre una terminal en esta carpeta.
3. Ejecuta `python main.py` (en algunos Windows, `py -3 main.py`).

El archivo `main.py` es un acceso sencillo para empezar. Como en FlashFood,
también puedes instalar el proyecto desde esta carpeta con `python -m pip install -e .`
y abrirlo con el comando `carwash`. Esta instalación puede necesitar descargar
`setuptools` si no está presente.

Para abrirlo con `main.py` no requiere paquetes externos. Los datos se guardan
automáticamente en `data/carwash.json` cuando se usa por primera vez. Para ejecutar
las pruebas sin instalar el paquete, usa PowerShell desde esta carpeta:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

## Qué hace

- Registra clientes junto a su vehículo (uno por cliente en esta primera versión).
- Incluye cuatro servicios iniciales con precios configurados y permite agregar otros.
- Calcula el precio mediante `calcular_precio()`. `ServicioPremium` hereda de
  `Servicio` y suma su recargo.
- Permite buscar horas libres de 09:00 a 18:00. Se supone **un solo puesto de lavado**.
- Al crear una cita calcula automáticamente hora de término y precio, y evita solapamientos.
- Gestiona los estados: Pendiente → Confirmado → En proceso → Finalizado. Una cita
  pendiente o confirmada se puede cancelar. Al reprogramarla vuelve a Pendiente.
- Conserva clientes, servicios y citas al cerrar la ventana mediante un archivo JSON.

## Carpetas, explicado sencillo

| Lugar | Responsabilidad |
| --- | --- |
| `main.py` | Acceso sencillo para iniciar la aplicación. |
| `pyproject.toml` | Describe el proyecto para instalarlo como paquete Python. |
| `src/carwash/__main__.py` | Inicio propio del paquete. |
| `src/carwash/modelo/` | Clases y reglas de negocio; no conoce la ventana. |
| `src/carwash/controladores/` | Recibe acciones de la ventana y llama al modelo. |
| `src/carwash/vista/` | Contiene una pantalla por archivo y los elementos visuales compartidos. |
| `src/carwash/persistencia/` | Lee y guarda el archivo JSON. |
| `data/` | Datos que genera el programa. |
| `tests/` | Pruebas automáticas del comportamiento. |
| `docs/` | Guía y diagrama para estudiar el proyecto. |

Para seguir el recorrido de una cita, lee la [guía paso a paso](docs/guia-paso-a-paso.md).
El [diagrama de clases](docs/diagrama-clases.md) muestra las relaciones principales.

Dentro de `vista/`, `aplicacion.py` reúne las pestañas; `inicio.py`, `clientes.py`,
`servicios.py` y `agenda.py` construyen cada pantalla. `comun.py` contiene la tabla,
los campos y el formato de pesos que usan varias pantallas.

## Límites de esta etapa

El sistema se concentra en **agendar lavados**. Todavía no cobra pagos reales ni
envía correos o mensajes. RUT y correo se validan por formato básico; no se comprueba
el dígito verificador del RUT. Los servicios iniciales se cargan en una instalación
nueva y se pueden agregar servicios adicionales desde la ventana.
