<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > crearReferenciaBibliografica()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearReferenciaBibliografica/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/crearReferenciaBibliografica/README.md)|[Desarrollo](/RUP/04-desarrollo/casos-uso/crearReferenciaBibliografica/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`crearReferenciaBibliografica()`](/RUP/01-requisitos/03-detalle-casos-uso/crearReferenciaBibliografica/README.md): CRUD real e inmediato contra `ReferenciaBibliograficaRepository`, sin ninguna interacción con `Guia`. La fila se crea con `guiaId` desde el principio (pertenece a esta `Guia` desde el momento de crearse), pero no queda **vinculada** a la colección oficial de la `Guia` hasta que [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md)/[`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) la vincule. Sin `<<choice>>` -- `ReferenciaBibliografica` no tiene ninguna regla de negocio documentada en el modelo de dominio.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/crearReferenciaBibliografica/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `CrearReferenciaBibliograficaView`

**Responsabilidades:**
- presenta el formulario de creación: `tipo` (enum en forma legible) y `referencia` (texto libre), ambos obligatorios.
- permite solicitar crear.

**Colaboraciones:**
- **Entrada:** `:REFERENCIAS_BIBLIOGRAFICAS_ABIERTO` -- el `Profesor` solicita crear una referencia para la `Guia` que tiene abierta.
- **Control:** `ReferenciaBibliograficaController`.
- **Salida:** `:Collaboration EditarReferenciaBibliografica` vía `<<include>> editarReferenciaBibliografica()`.

## Clases de controlador

### `ReferenciaBibliograficaController`

**Responsabilidades:**
- valida que `tipo` y `referencia` estén presentes (`validarDatosObligatorios`).
- crea la `ReferenciaBibliografica` directamente en `ReferenciaBibliograficaRepository`, real e inmediato -- ninguna llamada a `Guia`.

**Colaboraciones:**
- **Entrada:** `CrearReferenciaBibliograficaView`.
- **Salida:** `ReferenciaBibliograficaRepository`.

## Clases de modelo

### `ReferenciaBibliografica`

**Responsabilidades:**
- porta `tipo` (enum cerrado de cuatro valores), `referencia` (texto libre) y `guiaId` -- pertenece a una `Guia` desde su creación, aunque todavía no esté vinculada a su colección oficial.

**Colaboraciones:**
- **Entrada:** creada por `ReferenciaBibliograficaRepository`.

### `ReferenciaBibliograficaRepository`

**Responsabilidades:**
- crea la `ReferenciaBibliografica` (`crear(guiaId, tipo, referencia)`) -- persistencia real e inmediata, no una mutación de sesión.

**Colaboraciones:**
- **Entrada:** `ReferenciaBibliograficaController`.
- **Salida:** gestiona `ReferenciaBibliografica`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearReferenciaBibliografica/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/crearReferenciaBibliografica/wireframes.puml) -- fuente de verdad del formulario.
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `REFERENCIAS_BIBLIOGRAFICAS_ABIERTO --> REFERENCIA_BIBLIOGRAFICA_ABIERTO : crearReferenciaBibliografica()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Guia *-- ReferenciaBibliografica`, `ReferenciaBibliografica{tipo, referencia}`.
- [`abrirGuia()`](../abrirGuia/README.md) -- quien fusiona lo vinculado con lo pendiente-sin-vincular para presentarlo.
- [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) / [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) -- quienes vinculan esta fila a la colección oficial de la `Guia`.
