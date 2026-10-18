<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > importarBibliografiaDeGuiaHermana()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/importarBibliografiaDeGuiaHermana/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/importarBibliografiaDeGuiaHermana/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`importarBibliografiaDeGuiaHermana()`](/RUP/01-requisitos/03-detalle-casos-uso/importarBibliografiaDeGuiaHermana/README.md): el `Profesor` de una `AsignaturaPrograma` copia la bibliografía de una `Guia` importable de una `AsignaturaPrograma` hermana -- `Aprobada`, la imparta o no quien importa, o `EnRevision` solo si el `Profesor` también imparte la `AsignaturaPrograma` de la guía origen; nunca `Borrador` ni `Rechazada` (issue [#740](https://github.com/mmasias/pyCelda/issues/740), 2026-10-09; regla completa en [Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/importarBibliografiaDeGuiaHermana/README.md)). La hermana es otra con `id` distinto, el mismo `asignaturaId` no nulo y el mismo `Asignatura.codigo` (issue [#184](https://github.com/mmasias/pyCelda/issues/184), sobre la FK al catálogo puesta en el [#181](https://github.com/mmasias/pyCelda/issues/181)). Copia con **reemplazo total**: borra TODAS las `ReferenciaBibliografica` de la guía destino -- las vinculadas y las que el profesor destino tecleó a mano -- y crea filas nuevas con `guiaId` = destino copiando `tipo` y `referencia`, replicando el flag `vinculada` de cada fila origen TAL CUAL -- no se fuerza a `True`. Un origen `Aprobado` por el flujo normal (`enviar -> aprobar`) o `EnRevision` tiene todas las filas vinculadas (lo garantiza la regla `c1` de `enviarGuiaARevision`), así que sus copias también; sólo un origen que llegó a `Aprobada` vía `escalarGuiaAAprobada()` (que bypasea `c1`) puede llevar candidatas `vinculada=False` que el destino heredaría. Real e inmediata -- persiste en el acto en un solo commit, a diferencia del CRUD de L8 que queda en memoria hasta [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md). Si la guía destino estaba `Aprobada`, se degrada a `Borrador` (mismo mecanismo que `guardarBorradorGuia()` -> `Guia.confirmar_guardado()`) y la operación completa registra UNA fila de `HistorialCambio` (`campo="bibliografia"`, origen identificado en `comentario`, p.ej. "bibliografía importada desde GII / IYA003"). Autorización: relajación acotada de la regla 404-uniforme -- el `Profesor` de la `AsignaturaPrograma` destino puede LEER la bibliografía de una guía importable (`Aprobada`, o `EnRevision` de una `AsignaturaPrograma` que también imparte) de una hermana suya, sólo para listar y elegir origen y revalidarlo al importar; ninguna otra lectura cross-programa se abre. Importar es una copia, no un enlace: si después el origen se rechaza, se revoca o cambia, el destino no se entera. La previsualización del contenido fila a fila del origen antes de importar queda DIFERIDA a un refinamiento posterior: por ahora la vista informa con recuentos (referencias que trae el origen, referencias del destino que se reemplazarán).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/importarBibliografiaDeGuiaHermana/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `ImportarBibliografiaDeGuiaHermanaView`

**Responsabilidades:**
- presenta el desplegable de guías origen candidatas: las guías importables de `AsignaturaPrograma` hermanas, cada una identificada por programa + código de `Asignatura` + nombre de la AG hermana + estado con su fecha ("aprobada el ..." o "en revisión desde ..."), con el recuento de referencias que trae y el recuento de referencias del destino que se reemplazarán.
- permite solicitar importar.

**Colaboraciones:**
- **Entrada:** `:REFERENCIAS_BIBLIOGRAFICAS_ABIERTO` -- el `Profesor` solicita importar la bibliografía de una guía hermana para la `Guia` que tiene abierta; si no hay ninguna guía hermana importable, el caso de uso no se ofrece (botón ausente).
- **Control:** `ImportarBibliografiaDeGuiaHermanaController`.
- **Salida:** `:Collaboration AbrirReferenciasBibliograficas` vía `<<include>> abrirReferenciasBibliograficas()` -- vuelve al listado, ya con la bibliografía reemplazada.

## Clases de controlador

### `ImportarBibliografiaDeGuiaHermanaController`

**Responsabilidades:**
- `listarOrigenesImportables(guiaDestinoId)`: guías importables de hermanas con su estado, fecha y recuentos -- alimenta el desplegable; lista vacía = botón ausente. De las candidatas `Aprobadas` o `EnRevision` del `CursoAcademico` activo, conserva las `Aprobadas` y solo las `EnRevision` cuya `AsignaturaPrograma` también imparte el `Profesor` (`AsignaturaProgramaRepository.imparte()`).
- vuelve a obtener la `Guia` origen por id (`GuiaRepository.obtener(guiaOrigenId)`) y `validarHermandad(guiaDestino, guiaOrigen)`: revalidación server-side -- comprueba que la guía origen es importable (`Aprobada`, o `EnRevision` de una `AsignaturaPrograma` que el `Profesor` también imparte) y que la `AsignaturaPrograma` de origen sigue siendo hermana de la de destino (mismo `asignaturaId` no nulo y mismo `Asignatura.codigo`). El `guiaOrigenId` del cliente nunca se confía; el detalle de la respuesta (404 uniforme si no valida) se fija en Diseño.
- `importarBibliografia(guiaDestinoId, guiaOrigenId)`: orquesta el reemplazo -- borra todas las `ReferenciaBibliografica` del destino, crea copias desde el origen replicando `vinculada`, degrada la guía destino si estaba `Aprobada` y registra una fila de `HistorialCambio`.
- real e inmediato: toda la operación persiste en un solo commit.

**Colaboraciones:**
- **Entrada:** `ImportarBibliografiaDeGuiaHermanaView`.
- **Salida:** `GuiaRepository`, `AsignaturaProgramaRepository`, `Guia`, `ReferenciaBibliograficaRepository`, `HistorialCambio`.

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
- `imparte(asignaturaProgramaId, profesorId)`: si el `Profesor` imparte esa `AsignaturaPrograma` -- la misma comprobación que autoriza el destino, aplicada aquí a la guía origen `EnRevision` (issue #740).

**Colaboraciones:**
- **Entrada:** `ImportarBibliografiaDeGuiaHermanaController`.
- **Salida:** gestiona `AsignaturaPrograma`.

### `Guia`

**Responsabilidades:**
- `confirmar_guardado()`: degrada `Aprobada -> Borrador` si la guía destino estaba aprobada -- mecanismo reutilizado tal cual de `guardarBorradorGuia()`, la propia `Guia` decide según su máquina de estados.

**Colaboraciones:**
- **Entrada:** `ImportarBibliografiaDeGuiaHermanaController`.
- **Salida:** persistida por `GuiaRepository`.

### `GuiaRepository`

**Responsabilidades:**
- localiza la guía destino (`obtener(guiaDestinoId)`) y las guías `Aprobadas` o `EnRevision` de las hermanas en el `CursoAcademico` activo (`listarImportablesDe(hermanas, cursoAcademicoId)`); el filtro de "imparte" para las `EnRevision` lo aplica el controlador, no esta consulta.
- persiste la `Guia` tras el reemplazo -- posible cambio de `estado` (`actualizar(guia)`).

**Colaboraciones:**
- **Entrada:** `ImportarBibliografiaDeGuiaHermanaController`.
- **Salida:** gestiona `Guia`.

### `ReferenciaBibliografica`

**Responsabilidades:**
- porta `tipo`, `referencia`, `vinculada` y `guiaId` -- las copias nacen como filas nuevas con `guiaId` = destino y `vinculada` replicada fila a fila del origen.

**Colaboraciones:**
- **Entrada:** leídas las del origen y creadas las del destino por `ReferenciaBibliograficaRepository`.

### `ReferenciaBibliograficaRepository`

**Responsabilidades:**
- `reemplazarDesde(guiaDestinoId, referenciasOrigen)`: borra todas las `ReferenciaBibliografica` del destino (vinculadas y no vinculadas) y crea las copias (`tipo`, `referencia`, `vinculada`) -- persistencia real, parte del único commit de la operación.

**Colaboraciones:**
- **Entrada:** `ImportarBibliografiaDeGuiaHermanaController`.
- **Salida:** gestiona `ReferenciaBibliografica`.

### `HistorialCambio`

**Responsabilidades:**
- `registrar(campo="bibliografia", ...)`: UNA fila por la operación completa -- no una por referencia -- con el origen identificado en `comentario` (p.ej. "bibliografía importada desde GII / IYA003").

**Colaboraciones:**
- **Entrada:** creada por `ImportarBibliografiaDeGuiaHermanaController`.
- **Salida:** fila asociada a la `Guia` destino.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/importarBibliografiaDeGuiaHermana/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/importarBibliografiaDeGuiaHermana/wireframes.puml) -- fuente de verdad del desplegable de orígenes.
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `REFERENCIAS_BIBLIOGRAFICAS_ABIERTO --> REFERENCIAS_BIBLIOGRAFICAS_ABIERTO : importarBibliografiaDeGuiaHermana()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Guia *-- ReferenciaBibliografica`, `ReferenciaBibliografica{tipo, referencia}`; hermandad vía `AsignaturaPrograma.asignaturaId`.
- [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) -- mecanismo de degradado `Aprobada -> Borrador` compartido (`confirmar_guardado()`).
- [`abrirReferenciasBibliograficas()`](../abrirReferenciasBibliograficas/README.md) -- pantalla de origen del botón y retorno tras importar.
- [Issue #184](https://github.com/mmasias/pyCelda/issues/184) -- origen del caso de uso.
- [Issue #740](https://github.com/mmasias/pyCelda/issues/740) -- orígenes importables: `Aprobada`, o `EnRevision` que quien importa también imparte.
