# Clases principales de CarWash

```mermaid
classDiagram
    class Vehiculo {
        patente
        marca
        modelo
    }
    class Cliente {
        codigo
        nombre
        rut
        correo
        telefono
        vehiculo
    }
    class Servicio {
        codigo
        nombre
        duracion_minutos
        valor_base
        calcular_precio()
    }
    class ServicioPremium {
        recargo_premium
        calcular_precio()
    }
    class Agendamiento {
        numero
        codigo_cliente
        codigo_servicio
        fecha
        hora_inicio
        hora_termino
        precio_total
        estado
    }
    class SistemaCarWash {
        registrar_cliente()
        horarios_libres()
        crear_agendamiento()
        reprogramar_agendamiento()
        cambiar_estado()
    }

    Cliente *-- Vehiculo
    Servicio <|-- ServicioPremium
    SistemaCarWash o-- Cliente
    SistemaCarWash o-- Servicio
    SistemaCarWash o-- Agendamiento
    Agendamiento ..> Cliente : codigo_cliente
    Agendamiento ..> Servicio : codigo_servicio
```

`ServicioPremium` hereda de `Servicio`. Cuando la agenda calcula el valor,
llama a `calcular_precio()`: el servicio normal devuelve el valor base y el
premium suma su recargo. El agendamiento guarda los códigos del cliente y
del servicio para relacionarlos con sus registros.
