# Cómo entender este CarWash

Esta versión está separada del proyecto Java. No necesitas borrar ni cambiar nada
en NetBeans. Python abre una ventana propia usando **Tkinter**, que viene con la
instalación normal de Python en Windows.

## Primero: el recorrido de una cita

1. En **Clientes** escribes los datos de una persona y su vehículo. El sistema les
   asigna un código como `CLI-001`. En esta versión cada cliente tiene un vehículo.
2. En **Servicios** ya aparecen cuatro servicios iniciales. Puedes agregar
   más. La duración está en minutos y los precios son números enteros de pesos.
3. En **Agenda** eliges cliente, servicio y fecha. **Ver horarios libres** consulta
   qué bloques caben según la duración del servicio.
4. **Crear cita** revisa que el horario sea futuro, que esté dentro de 09:00–18:00
   y que no choque con otra cita. Después calcula hora de término y precio.
5. La cita nace **Pendiente**. Al seleccionarla en la tabla puedes confirmarla,
   iniciar el lavado, finalizarlo o cancelarla. Reprogramar una cita confirmada
   la devuelve a Pendiente para volver a confirmar el nuevo horario.

## Segundo: cómo está dividido el código

Imagina que el programa se hace esta cadena de preguntas cuando presionas
**Crear cita**:

`src/carwash/vista/agenda.py` → `src/carwash/controladores/controlador.py` →
`src/carwash/modelo/sistema.py` → `src/carwash/persistencia/repositorio_json.py`

- **Vista**: muestra formularios, tablas y mensajes. Cada pantalla está en su propio
  archivo (`inicio.py`, `clientes.py`, `servicios.py` y `agenda.py`).
  `aplicacion.py` las reúne y `comun.py` evita repetir elementos visuales.
  La vista no decide si el horario es válido.
- **Controlador**: recibe lo que escribiste y pide la operación correspondiente.
- **Modelo**: conoce las reglas. Por ejemplo, detecta dos citas que se cruzan.
- **Persistencia**: guarda los resultados en un archivo JSON para que sigan ahí
  después de cerrar el programa.

La carpeta `src` indica dónde está el código del programa. El archivo `main.py`
inicia la aplicación de forma sencilla y `pyproject.toml` permite instalarla
como paquete, igual que FlashFood. Puedes seguir usando `python main.py`.

Esto se parece a la organización de FlashFood, pero se adaptó a la agenda CarWash.
No se copiaron las reglas de pedidos, reparto o stock porque son de otro negocio.

## Tercero: las clases principales

- `Vehiculo`: patente, marca y modelo. No tiene tamaño porque decidimos quitarlo.
- `Cliente`: sus datos personales y un `Vehiculo`.
- `Servicio`: nombre, duración y valor base. Su método `calcular_precio()`
  devuelve el valor base.
- `ServicioPremium`: es un tipo de `Servicio` (**herencia**). Tiene además
  un recargo y redefine `calcular_precio()` para sumarlo (**polimorfismo**).
- `Agendamiento`: une cliente y servicio con fecha, horas, precio y estado.
- `SistemaCarWash`: administra las listas de objetos y aplica las reglas.

En el catálogo inicial, el lavado full vale 15.000 y dura 60 minutos. El premium tiene
base 20.000 más 5.000 de recargo y termina en 90 minutos. El sistema llama
`calcular_precio()` de la misma forma en ambos, pero cada clase responde distinto.

## Cuarto: dónde se guarda

`data/carwash.json` es un archivo de texto estructurado. Lo crea el programa
y se actualiza automáticamente. No es código y normalmente no necesitas editarlo
a mano. Si se daña, el programa avisará en lugar de borrarlo.

## Qué todavía no hace

No hay pagos reales, envío de correos ni varias pistas de lavado. Esas serían
etapas posteriores. La prioridad de esta entrega es que la **agenda** funcione
de principio a fin y sea fácil de explicar.
