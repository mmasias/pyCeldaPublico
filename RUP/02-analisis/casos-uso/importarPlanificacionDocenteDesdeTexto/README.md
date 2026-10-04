<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > importarPlanificacionDocenteDesdeTexto()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/importarPlanificacionDocenteDesdeTexto/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/importarPlanificacionDocenteDesdeTexto/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`importarPlanificacionDocenteDesdeTexto()`](/RUP/01-requisitos/03-detalle-casos-uso/importarPlanificacionDocenteDesdeTexto/README.md) (issue [#552](https://github.com/mmasias/pyCelda/issues/552)): el `Profesor` pega un texto con una `Sesion` por línea (`CODIGO - Descripción`) y la planificación docente de la `Guia` abierta se reemplaza por la parseada. Hermano de [`importarPlanificacionDocenteDeGuiaHermana()`](/RUP/02-analisis/casos-uso/importarPlanificacionDocenteDeGuiaHermana/README.md) con otro origen: no hay hermandad, ni guía origen, ni lectura cross-programa. Copia con **reemplazo total**: borra TODAS las `Sesion` de la guía destino y crea filas nuevas con `guiaId` = destino, `vinculada=False`, numeradas 1..N en persistencia en el orden de las líneas, sin tocar `guia.sesiones_minimas`. Real e inmediata -- un solo commit. Si la guía destino estaba `Aprobada`, se degrada a `Borrador` (`Guia.confirmar_guardado()`) y se registra UNA fila de `HistorialCambio` (`campo="planificacion_docente"`, `comentario="planificación docente importada desde texto pegado"`). El parseo es una función pura sin acceso a datos (`ParserPlanificacionTexto`): con separador completo, código reconocido -> `Sesion.tipo` mapeado + parte derecha como descripción, código no reconocido -> `CLASE_TEORICA` con la línea completa; sin separador completo pero código reconocido (fila de tipo correcto sin contenido) -> mismo tipo con descripción vacía, nunca se descarta por falta de contenido; líneas vacías ignoradas.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/importarPlanificacionDocenteDesdeTexto/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `ImportarPlanificacionDocenteDesdeTextoView`

**Responsabilidades:**
- presenta la tabla de códigos reconocidos, el área de texto y el aviso de reemplazo (recuento de sesiones actuales; aviso adicional si el texto está vacío).
- permite solicitar importar.

**Colaboraciones:**
- **Entrada:** `:PLANIFICACION_DOCENTE_ABIERTO` -- el `Profesor` solicita importar desde texto la planificación docente de la `Guia` que tiene abierta.
- **Control:** `ImportarPlanificacionDocenteDesdeTextoController`.
- **Salida:** `:Collaboration AbrirPlanificacionDocente` vía `<<include>> abrirPlanificacionDocente()` -- vuelve al listado, ya reemplazado.

## Clases de controlador

### `ImportarPlanificacionDocenteDesdeTextoController`

**Responsabilidades:**
- `importarPlanificacionDocenteDesdeTexto(guiaDestinoId, texto)`: orquesta el reemplazo -- localiza la guía destino y comprueba que el `Profesor` la imparte (404 uniforme si no), parsea el texto, borra todas las `Sesion` del destino y crea las nuevas 1..N, degrada la guía si estaba `Aprobada` y registra una fila de `HistorialCambio`.
- real e inmediato: toda la operación persiste en un solo commit.

**Colaboraciones:**
- **Entrada:** `ImportarPlanificacionDocenteDesdeTextoView`.
- **Salida:** `GuiaRepository`, `AsignaturaProgramaRepository`, `ParserPlanificacionTexto`, `Guia`, `SesionRepository`, `HistorialCambio`.

## Clases de modelo

### `ParserPlanificacionTexto`

**Responsabilidades:**
- `parsear(texto)`: lista de `(tipo, descripcion)`, una por línea no vacía; corta por la primera ocurrencia de ` - `, normaliza el código con `strip()` + `upper()` y lo mapea a `Sesion.tipo`; sin ese separador, si lo que queda tras un guion final es un código reconocido se respeta igualmente (descripción vacía); sin código reconocido en ningún caso, `CLASE_TEORICA` con la línea completa.

**Colaboraciones:**
- **Entrada:** `ImportarPlanificacionDocenteDesdeTextoController`.

### `AsignaturaProgramaRepository`

**Responsabilidades:**
- `imparte(asignaturaProgramaId, profesorId)`: comprueba que el `Profesor` imparte la `AsignaturaPrograma` de la guía destino.

**Colaboraciones:**
- **Entrada:** `ImportarPlanificacionDocenteDesdeTextoController`.

### `Guia`

**Responsabilidades:**
- `confirmar_guardado()`: degrada `Aprobada -> Borrador` si la guía destino estaba aprobada -- mecanismo reutilizado de `guardarBorradorGuia()`.

**Colaboraciones:**
- **Entrada:** `ImportarPlanificacionDocenteDesdeTextoController`.
- **Salida:** persistida por `GuiaRepository`.

### `GuiaRepository`

**Responsabilidades:**
- localiza la guía destino (`obtener(guiaDestinoId)`).

**Colaboraciones:**
- **Entrada:** `ImportarPlanificacionDocenteDesdeTextoController`.
- **Salida:** gestiona `Guia`.

### `Sesion`

**Responsabilidades:**
- porta `numero`, `tipo`, `descripcion`, `vinculada` y `guiaId` -- las nuevas nacen con `guiaId` = destino, `vinculada=False` y `numero` 1..N en el orden de las líneas.

**Colaboraciones:**
- **Entrada:** creadas en el destino por `SesionRepository`.

### `SesionRepository`

**Responsabilidades:**
- `reemplazarDesde(guiaDestino, sesiones)`: borra todas las `Sesion` del destino y crea las nuevas renumeradas 1..N en persistencia -- mismo método que [`importarPlanificacionDocenteDeGuiaHermana()`](/RUP/02-analisis/casos-uso/importarPlanificacionDocenteDeGuiaHermana/README.md); no toca `Guia.sesiones_minimas`.

**Colaboraciones:**
- **Entrada:** `ImportarPlanificacionDocenteDesdeTextoController`.
- **Salida:** gestiona `Sesion`.

### `HistorialCambio`

**Responsabilidades:**
- `registrar(campo="planificacion_docente", ...)`: UNA fila por la operación completa, con `valor_nuevo="N sesiones (texto pegado)"`.

**Colaboraciones:**
- **Entrada:** creada por `ImportarPlanificacionDocenteDesdeTextoController`.
- **Salida:** fila asociada a la `Guia` destino.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/importarPlanificacionDocenteDesdeTexto/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/importarPlanificacionDocenteDesdeTexto/wireframes.puml).
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `PLANIFICACION_DOCENTE_ABIERTO --> PLANIFICACION_DOCENTE_ABIERTO : importarPlanificacionDocenteDesdeTexto()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Guia *-- PlanificacionDocente *-- Sesion` (divergencia lateral con el `Sesion.guia_id` directo del código).
- [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) -- mecanismo de degradado `Aprobada -> Borrador` compartido.
- [`abrirPlanificacionDocente()`](../abrirPlanificacionDocente/README.md) -- pantalla de origen del botón y retorno tras importar.
- [Issue #552](https://github.com/mmasias/pyCelda/issues/552) -- origen del caso de uso.
