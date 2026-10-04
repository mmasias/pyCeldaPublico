<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > importarContenidoDeGuiaHermana()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/importarContenidoDeGuiaHermana/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/importarContenidoDeGuiaHermana/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`importarContenidoDeGuiaHermana()`](/RUP/01-requisitos/03-detalle-casos-uso/importarContenidoDeGuiaHermana/README.md) (issue [#409](https://github.com/mmasias/pyCelda/issues/409)): el `Profesor` de una `AsignaturaPrograma` reemplaza el `contenido` (temario) de la `Guia` que tiene abierta con el de una `Guia` en estado `Aprobada` de una `AsignaturaPrograma` hermana -- otra con `id` distinto, el mismo `asignaturaId` no nulo y el mismo `Asignatura.codigo` (familia del issue [#184](https://github.com/mmasias/pyCelda/issues/184)). Calca [`importarBibliografiaDeGuiaHermana()`](../importarBibliografiaDeGuiaHermana/README.md) con tres diferencias reales: (1) `contenido` es un **campo escalar de la propia `Guia`**, sin colección que gestionar -- no hay `ReferenciaBibliograficaRepository` ni equivalente, y la copia se hace con `Guia.actualizarContenido()`; (2) es un **self-loop directo de `GUIA_ABIERTO`**, no de un listado propio, y **no hay `<<include>>`** de vuelta: la pantalla no cambia, el control vive inline en la de `abrirGuia()`; (3) la fila de `HistorialCambio` es de `campo="contenido"` -- campo ya existente, compartido con la edición manual -- y **solo se registra si el contenido cambió**. Reemplazo total (no fusiona), real e inmediato en un solo commit. Si la guía destino estaba `Aprobada`, se degrada a `Borrador` (mismo mecanismo que `guardarBorradorGuia()` -> `Guia.confirmarGuardado()`). Autorización: la misma relajación acotada de la regla 404-uniforme que el resto de la familia -- el `Profesor` de la `AsignaturaPrograma` destino puede leer guías `Aprobadas` de sus hermanas del curso **activo**, solo para listar y elegir origen. Caso de uso reutilizado por `DirectorPrograma` (hereda de `Profesor`); el actor efectivo es siempre el `Profesor` de la `AsignaturaPrograma` destino.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/importarContenidoDeGuiaHermana/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `ImportarContenidoDeGuiaHermanaView`

**Responsabilidades:**
- presenta el desplegable de guías origen candidatas -- las `Aprobadas` de `AsignaturaPrograma` hermanas del curso activo, cada una identificada por código de `Asignatura` + programa + nombre de la `AsignaturaPrograma` hermana -- y el botón de importar, deshabilitado hasta elegir origen. Sin recuento de referencias ni fecha de aprobación en la opción (a diferencia de bibliografía) y sin previsualización del contenido.
- tras elegir origen, avisa de que importar **reemplaza el contenido actual, incluidos los cambios sin guardar**.
- tras importar, actualiza el `contenido` local de la pantalla con la respuesta, para que un guardado posterior no pise en silencio lo recién importado con el valor viejo que seguía en el campo de texto.
- el control no se ofrece cuando no hay ninguna guía hermana `Aprobada`, ni en modo revisión (`DirectorPrograma` evaluando la `Guia` de otro).

**Colaboraciones:**
- **Entrada:** `:GUIA_ABIERTO` -- el `Profesor` solicita importar el contenido de una guía hermana para la `Guia` que tiene abierta.
- **Control:** `ImportarContenidoDeGuiaHermanaController`.
- **Salida:** `:GUIA_ABIERTO` -- self-loop sobre la misma pantalla, ya con el `contenido` reemplazado (sin `<<include>>` ni navegación).

## Clases de controlador

### `ImportarContenidoDeGuiaHermanaController`

**Responsabilidades:**
- `listarOrigenesImportables(guiaDestinoId)`: guías `Aprobadas` de hermanas del curso activo -- alimenta el desplegable; lista vacía = control ausente.
- vuelve a obtener la `Guia` origen por id (`GuiaRepository.obtener(guiaOrigenId)`) y `validarHermandad(guiaDestino, guiaOrigen)`: revalidación server-side -- comprueba que `guiaOrigen.estado == "Aprobada"`, que pertenece al curso activo y que su `AsignaturaPrograma` sigue siendo hermana de la de destino (mismo `asignaturaId` no nulo y mismo `Asignatura.codigo`). El `guiaOrigenId` del cliente nunca se confía; el detalle de la respuesta (404 uniforme si no valida) se fija en Diseño.
- `importarContenido(guiaDestinoId, guiaOrigenId)`: orquesta el reemplazo -- pide a la `Guia` destino que adopte el `contenido` del origen, registra una fila de `HistorialCambio` solo si el texto cambió, degrada la guía destino si estaba `Aprobada` y persiste.
- real e inmediato: toda la operación persiste en un solo commit.

**Colaboraciones:**
- **Entrada:** `ImportarContenidoDeGuiaHermanaView`.
- **Salida:** `GuiaRepository`, `AsignaturaProgramaRepository`, `CursoAcademicoRepository`, `Guia`, `HistorialCambio`.

## Clases de modelo

### `AsignaturaPrograma`

**Responsabilidades:**
- porta `asignaturaId` (FK al catálogo `Asignatura`, issue [#181](https://github.com/mmasias/pyCelda/issues/181)) -- dos `AsignaturaPrograma` con el mismo `asignaturaId` y el mismo `Asignatura.codigo` son hermanas.

**Colaboraciones:**
- **Entrada:** gestionada por `AsignaturaProgramaRepository`.
- **Salida:** su hermandad resuelve qué guías origen son importables.

### `AsignaturaProgramaRepository`

**Responsabilidades:**
- `listarHermanas(asignaturaProgramaId)`: otras `AsignaturaPrograma` con el mismo `asignaturaId` y el mismo `codigo`, excluyendo la propia; `[]` si `asignaturaId` es nulo.
- `imparte(asignaturaProgramaId, profesorId)`: base de la autorización -- el `Profesor` debe impartir la `AsignaturaPrograma` destino.

**Colaboraciones:**
- **Entrada:** `ImportarContenidoDeGuiaHermanaController`.
- **Salida:** gestiona `AsignaturaPrograma`.

### `CursoAcademicoRepository`

**Responsabilidades:**
- `activo(universidadId)`: el `CursoAcademico` activo -- acota los orígenes importables. Siempre el activo, sin selector: importar es una escritura que reemplaza contenido real de la `Guia` destino.

**Colaboraciones:**
- **Entrada:** `ImportarContenidoDeGuiaHermanaController`.
- **Salida:** gestiona `CursoAcademico`.

### `Guia`

**Responsabilidades:**
- porta `contenido` (el temario, texto libre) y `estado`.
- `actualizarContenido(contenido)`: sustituye el `contenido` y devuelve el valor anterior **solo si el texto cambió**, o nada si llega idéntico -- el historial arranca con la primera acción humana real.
- `confirmarGuardado()`: degrada `Aprobada -> Borrador` si la guía destino estaba aprobada -- mecanismo reutilizado tal cual de `guardarBorradorGuia()`, la propia `Guia` decide según su máquina de estados.

**Colaboraciones:**
- **Entrada:** `ImportarContenidoDeGuiaHermanaController`.
- **Salida:** persistida por `GuiaRepository`.

### `GuiaRepository`

**Responsabilidades:**
- localiza la guía destino (`obtener(guiaDestinoId)`) y las guías `Aprobadas` de las hermanas del curso activo (`listarAprobadasDe(hermanas, cursoAcademicoId)`).
- persiste la `Guia` tras el reemplazo -- nuevo `contenido` y posible cambio de `estado`.

**Colaboraciones:**
- **Entrada:** `ImportarContenidoDeGuiaHermanaController`.
- **Salida:** gestiona `Guia`.

### `HistorialCambio`

**Responsabilidades:**
- `registrar(campo="contenido", ...)`: UNA fila por la operación, **solo si el contenido cambió** (sin fila si el texto importado es idéntico al actual), con el origen identificado en `comentario` (p.ej. "contenido importado desde GII / IYA003"). `valorAnterior`/`valorNuevo` guardan un resumen corto del temario, no el texto completo -- el detalle vive en `Guia.contenido`.

**Colaboraciones:**
- **Entrada:** creada por `ImportarContenidoDeGuiaHermanaController`.
- **Salida:** fila asociada a la `Guia` destino.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/importarContenidoDeGuiaHermana/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/importarContenidoDeGuiaHermana/wireframes.puml) -- fuente de verdad del control inline y de la decisión de "sin pantalla propia".
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `GUIA_ABIERTO --> GUIA_ABIERTO : importarContenidoDeGuiaHermana()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Guia { contenido }`, `Guia *-- HistorialCambio`; hermandad vía `AsignaturaPrograma.asignaturaId`.
- [`importarBibliografiaDeGuiaHermana()`](../importarBibliografiaDeGuiaHermana/README.md) -- plantilla de la que se calca este caso de uso, con colección en vez de campo escalar.
- [`importarPlanificacionDocenteDeGuiaHermana()`](../importarPlanificacionDocenteDeGuiaHermana/README.md) -- el otro gemelo de la familia #184.
- [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) -- `Guia.actualizarContenido()` y mecanismo de degradado `Aprobada -> Borrador` compartidos.
- [`abrirGuia()`](../abrirGuia/README.md) -- pantalla donde vive el control inline.
- [Issue #409](https://github.com/mmasias/pyCelda/issues/409) -- origen del caso de uso.
