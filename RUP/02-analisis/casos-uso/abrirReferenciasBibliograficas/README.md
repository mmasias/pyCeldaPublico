<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > abrirReferenciasBibliograficas()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirReferenciasBibliograficas/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirReferenciasBibliograficas/README.md)|[Desarrollo](/RUP/04-desarrollo/casos-uso/abrirReferenciasBibliograficas/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirReferenciasBibliograficas()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirReferenciasBibliograficas/README.md): un solo paso, sin `<<choice>>`, de solo lectura -- no vincula nada. Presenta el listado completo de `ReferenciaBibliografica` de la `Guia` abierta, **fusionando** lo ya vinculado con lo pendiente-sin-vincular creado en [`crearReferenciaBibliografica()`](../crearReferenciaBibliografica/README.md), agrupado por `tipo`. Mismo mecanismo de fusión que [`abrirGuia()`](../abrirGuia/README.md) y [`abrirPonderacionesEvaluacion()`](../abrirPonderacionesEvaluacion/README.md), aplicado aquí a `ReferenciaBibliografica`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirReferenciasBibliograficas/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirReferenciasBibliograficasView`

**Responsabilidades:**
- presenta el listado de `ReferenciaBibliografica` de la `Guia`, agrupado por `tipo`.
- ofrece la navegación a crear una nueva referencia, a abrir/eliminar cada fila, y a volver a la `Guia`.

**Colaboraciones:**
- **Entrada:** `:GUIA_ABIERTO` -- el `Profesor` solicita abrir el listado de referencias desde la `Guia`; `:REFERENCIA_BIBLIOGRAFICA_ABIERTO` -- el `Profesor` solicita volver al listado desde el detalle de una referencia. Mismo caso de uso invocado desde ambos puntos.
- **Control:** `ReferenciaBibliograficaController`.
- **Salida:** `:REFERENCIAS_BIBLIOGRAFICAS_ABIERTO`.

## Clases de controlador

### `ReferenciaBibliograficaController`

**Responsabilidades:**
- pide, para la `Guia`, las `ReferenciaBibliografica` ya vinculadas y las pendientes-sin-vincular por separado, y las fusiona en una sola lista por presentar -- mismo criterio que `GuiaController` en `abrirGuia()`: unión simple, sin regla de negocio.
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirReferenciasBibliograficasView`.
- **Salida:** `ReferenciaBibliograficaRepository`.

## Clases de modelo

### `ReferenciaBibliografica`

**Responsabilidades:**
- porta `tipo`, `referencia` y si está vinculada -- mostrada agrupada por tipo, fusionando vinculadas y pendientes.

**Colaboraciones:**
- **Entrada:** listada por `ReferenciaBibliograficaRepository`, vinculada o pendiente.

### `ReferenciaBibliograficaRepository`

**Responsabilidades:**
- lista las `ReferenciaBibliografica` vinculadas a la `Guia` (`listarVinculadasDe(guia)`).
- lista las `ReferenciaBibliografica` con este `guiaId` todavía sin vincular (`listarPendientesDe(guiaId)`).

**Colaboraciones:**
- **Entrada:** `ReferenciaBibliograficaController`.
- **Salida:** gestiona `ReferenciaBibliografica`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirReferenciasBibliograficas/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirReferenciasBibliograficas/wireframes.puml) -- fuente de verdad del listado agrupado por tipo.
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `GUIA_ABIERTO --> REFERENCIAS_BIBLIOGRAFICAS_ABIERTO : abrirReferenciasBibliograficas()`, `REFERENCIA_BIBLIOGRAFICA_ABIERTO --> REFERENCIAS_BIBLIOGRAFICAS_ABIERTO : abrirReferenciasBibliograficas()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Guia *-- ReferenciaBibliografica`.
- [`abrirGuia()`](../abrirGuia/README.md) -- mismo mecanismo de fusión vinculado+pendiente, aplicado a cada colección de la Guía.
- [`crearReferenciaBibliografica()`](../crearReferenciaBibliografica/README.md) / [`eliminarReferenciaBibliografica()`](../eliminarReferenciaBibliografica/README.md) / [`editarReferenciaBibliografica()`](../editarReferenciaBibliografica/README.md) -- quienes crean, quitan o editan lo que este listado presenta.
- [`abrirReferenciaBibliografica()`](../abrirReferenciaBibliografica/README.md) -- detalle de solo lectura de una fila, alcanzado desde este listado.
