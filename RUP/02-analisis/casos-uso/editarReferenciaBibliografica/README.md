<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > editarReferenciaBibliografica()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarReferenciaBibliografica/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarReferenciaBibliografica/README.md)|[Desarrollo](/RUP/04-desarrollo/casos-uso/editarReferenciaBibliografica/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`editarReferenciaBibliografica()`](/RUP/01-requisitos/03-detalle-casos-uso/editarReferenciaBibliografica/README.md): CRUD real e inmediato contra `ReferenciaBibliograficaRepository`, sin ninguna interacción con `Guia`. A diferencia de [`editarPonderacionEvaluacion()`](../editarPonderacionEvaluacion/README.md), sin `<<choice>>` de negocio -- `ReferenciaBibliografica` no tiene ninguna regla de validación cruzada documentada en el modelo de dominio, solo obligatorios (`tipo`, `referencia`). Cierra el hueco que el [diagrama de clases consolidado](/RUP/02-analisis/diagrama-clases-analisis.puml) señalaba explícitamente: `ReferenciaBibliografica` gana aquí su método `actualizar()`, simétrico a `PonderacionEvaluacion.actualizar()`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarReferenciaBibliografica/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarReferenciaBibliograficaView`

**Responsabilidades:**
- presenta el formulario con los datos actuales de la referencia (`tipo`, `referencia`).
- permite solicitar guardar.

**Colaboraciones:**
- **Entrada:** `:REFERENCIA_BIBLIOGRAFICA_ABIERTO` -- el `Profesor` solicita editar la referencia abierta.
- **Control:** `ReferenciaBibliograficaController`.
- **Salida:** `:REFERENCIA_BIBLIOGRAFICA_ABIERTO`.

## Clases de controlador

### `ReferenciaBibliograficaController`

**Responsabilidades:**
- recupera la `ReferenciaBibliografica` a editar (`cargarReferenciaBibliografica(referenciaId)`, mismo método introducido por [`abrirReferenciaBibliografica()`](../abrirReferenciaBibliografica/README.md)).
- valida los obligatorios (`validarDatosObligatorios(tipo, referencia)`).
- guarda los cambios (`guardarCambios(tipo, referencia)`): sin `<<choice>>` de negocio que aplicar, a diferencia de `PonderacionEvaluacionController` -- pide directamente a la `ReferenciaBibliografica` que se actualice y persiste.

**Colaboraciones:**
- **Entrada:** `EditarReferenciaBibliograficaView`.
- **Salida:** `ReferenciaBibliografica`, `ReferenciaBibliograficaRepository`.

## Clases de modelo

### `ReferenciaBibliografica`

**Responsabilidades:**
- porta `tipo` y `referencia`, ambos editables.
- se actualiza a sí misma (`actualizar(tipo, referencia)`) -- método nuevo, cierra la asimetría con `PonderacionEvaluacion.actualizar()` señalada como alcance pendiente en el diagrama de clases consolidado.

**Colaboraciones:**
- **Entrada:** `ReferenciaBibliograficaController`.
- **Salida:** persistida por `ReferenciaBibliograficaRepository`.

### `ReferenciaBibliograficaRepository`

**Responsabilidades:**
- recupera la `ReferenciaBibliografica` por identificador (`obtener(referenciaId)`).
- persiste la actualización (`actualizar(referencia)`) -- método nuevo.

**Colaboraciones:**
- **Entrada:** `ReferenciaBibliograficaController`.
- **Salida:** gestiona `ReferenciaBibliografica`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarReferenciaBibliografica/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarReferenciaBibliografica/wireframes.puml) -- fuente de verdad del formulario, sin rama de rechazo.
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `REFERENCIA_BIBLIOGRAFICA_ABIERTO --> REFERENCIA_BIBLIOGRAFICA_ABIERTO : editarReferenciaBibliografica()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ReferenciaBibliografica{tipo, referencia}`.
- [`crearReferenciaBibliografica()`](../crearReferenciaBibliografica/README.md) -- `<<include>>` de origen, ya cerrado apuntando aquí.
- [`abrirReferenciaBibliografica()`](../abrirReferenciaBibliografica/README.md) -- mismo `ReferenciaBibliograficaController.cargarReferenciaBibliografica(referenciaId)`, reutilizado.
- [`editarPonderacionEvaluacion()`](../editarPonderacionEvaluacion/README.md) -- contraste: sí tiene `<<choice>>` de negocio (máximo puntual del `SistemaEvaluacion`), este caso no.
- [Discussion #59](https://github.com/mmasias/pyCelda/discussions/59) -- señalaba esta asimetría como alcance, no como hueco, hasta que este caso de uso se construyera.
