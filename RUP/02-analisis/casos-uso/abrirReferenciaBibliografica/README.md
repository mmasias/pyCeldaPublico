<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > abrirReferenciaBibliografica()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirReferenciaBibliografica/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirReferenciaBibliografica/README.md)|[Desarrollo](/RUP/04-desarrollo/casos-uso/abrirReferenciaBibliografica/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirReferenciaBibliografica()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirReferenciaBibliografica/README.md): un solo paso, sin `<<choice>>`, de solo lectura -- muestra el detalle de una `ReferenciaBibliografica` concreta (`tipo`, `referencia`). Primer caso de uso que necesita cargar una `ReferenciaBibliografica` individual: ni `crearReferenciaBibliografica()` ni `eliminarReferenciaBibliografica()` releían la fila (la primera la crea, la segunda usa los datos ya conocidos del listado) -- este caso introduce `ReferenciaBibliograficaRepository.obtener(referenciaId)`, reutilizado después por [`editarReferenciaBibliografica()`](../editarReferenciaBibliografica/README.md).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirReferenciaBibliografica/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirReferenciaBibliograficaView`

**Responsabilidades:**
- presenta `tipo` (en forma legible) y `referencia` de la `ReferenciaBibliografica` abierta.
- ofrece la navegación a editar la referencia o volver al listado.

**Colaboraciones:**
- **Entrada:** `:REFERENCIAS_BIBLIOGRAFICAS_ABIERTO` -- el `Profesor` solicita abrir una `ReferenciaBibliografica` desde su fila en el listado.
- **Control:** `ReferenciaBibliograficaController`.
- **Salida:** `:REFERENCIA_BIBLIOGRAFICA_ABIERTO`.

## Clases de controlador

### `ReferenciaBibliograficaController`

**Responsabilidades:**
- recupera la `ReferenciaBibliografica` a mostrar (`cargarReferenciaBibliografica(referenciaId)`), método nuevo, reutilizado después por `editarReferenciaBibliografica()`.
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirReferenciaBibliograficaView`.
- **Salida:** `ReferenciaBibliograficaRepository`.

## Clases de modelo

### `ReferenciaBibliografica`

**Responsabilidades:**
- porta `tipo` (enum cerrado de cuatro valores) y `referencia` (texto libre) -- los datos mostrados, sin edición en este caso de uso.

**Colaboraciones:**
- **Entrada:** recuperada por `ReferenciaBibliograficaRepository`.

### `ReferenciaBibliograficaRepository`

**Responsabilidades:**
- recupera la `ReferenciaBibliografica` por identificador (`obtener(referenciaId)`) -- método nuevo, no necesario hasta ahora en la rebanada.

**Colaboraciones:**
- **Entrada:** `ReferenciaBibliograficaController`.
- **Salida:** gestiona `ReferenciaBibliografica`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirReferenciaBibliografica/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirReferenciaBibliografica/wireframes.puml) -- fuente de verdad del detalle de solo lectura.
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `REFERENCIAS_BIBLIOGRAFICAS_ABIERTO --> REFERENCIA_BIBLIOGRAFICA_ABIERTO : abrirReferenciaBibliografica()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ReferenciaBibliografica{tipo, referencia}`.
- [`editarReferenciaBibliografica()`](../editarReferenciaBibliografica/README.md) -- reutiliza `cargarReferenciaBibliografica(referenciaId)`, introducido aquí.
- [`abrirReferenciasBibliograficas()`](../abrirReferenciasBibliograficas/README.md) -- listado del que procede esta fila.
