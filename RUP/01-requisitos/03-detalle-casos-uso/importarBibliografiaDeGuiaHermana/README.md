<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > importarBibliografiaDeGuiaHermana()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/importarBibliografiaDeGuiaHermana/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/importarBibliografiaDeGuiaHermana/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor`|
|**Objetivo**|Reemplazar la bibliografía de la `Guia` abierta con la de una `Guia` `Aprobada` de una `AsignaturaGrado` hermana|
|**Tipo**|Primario|
|**Nivel**|Objetivo de usuario|

</div>

Caso de uso reutilizado por `DirectorGrado`, misma ficha -- ver [modelo del dominio](/RUP/00-modelo-del-dominio/README.md) (`DirectorGrado --|> Profesor`), no redeclarado, mismo trato que [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md). El actor efectivo es siempre el `Profesor` de la `AsignaturaGrado` **destino** -- la autorización se resuelve con la misma comprobación `imparte` que el resto del hilo de `Guia`.

**`AsignaturaGrado` hermana** (issue [#184](https://github.com/mmasias/pyCelda/issues/184)): otra `AsignaturaGrado`, de otro `Grado`, que comparte el mismo `Asignatura` del catálogo institucional -- **doble comprobación**: mismo `asignatura_id` (la FK real que puso el issue [#181](https://github.com/mmasias/pyCelda/issues/181), no nula) **y** mismo `Asignatura.codigo`. Es literalmente la misma asignatura del catálogo impartida en otra titulación. `nombre`, `contenido` y bibliografía pueden diverger legítimamente entre hermanas (medido en el piloto GII + GIOI: `IYA003` = "Programación I" en GII, "Informática" en GIOI) -- por eso importar es una acción deliberada del profesor, no una propagación automática. Si la `AsignaturaGrado` destino no tiene `asignatura_id` resuelto (dato legado sin reconciliar en el backfill de #181), no tiene hermanas y el caso de uso no se ofrece.

**Origen**: una `Guia` en estado `Aprobada` de una `AsignaturaGrado` hermana. Una `Guia` en `Borrador` de otro profesor no es fuente fiable. Si hay más de una hermana con guía aprobada, el `Profesor` elige en un desplegable, con el origen plenamente identificado (grado, código de asignatura, nombre de la `AsignaturaGrado` hermana, fecha de aprobación de la guía y número de referencias que trae). Si ninguna hermana tiene guía aprobada, el caso de uso no ofrece origen y el botón está ausente -- mismo criterio de disponibilidad condicional que `[Descargar PDF]` en [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md), de ahí que la especificación lleve un `<<choice>>` de salvaguarda estructural cuya rama roja no se dispara desde la interfaz.

**Copia con reemplazo total, real e inmediata** (a diferencia del CRUD de [`crearReferenciaBibliografica()`](../crearReferenciaBibliografica/README.md)/[`editarReferenciaBibliografica()`](../editarReferenciaBibliografica/README.md)/[`eliminarReferenciaBibliografica()`](../eliminarReferenciaBibliografica/README.md), que quedan en memoria hasta [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md)): la operación borra **todas** las `ReferenciaBibliografica` de la `Guia` destino -- las vinculadas y las que el profesor destino tecleó a mano -- y crea filas nuevas copiando `tipo` y `referencia` de las de la guía origen, replicando el flag `vinculada` de cada fila origen **tal cual**. Es una única operación atómica, un solo commit; no hay fusión con lo que había (generaría duplicados). El aviso del recuento a reemplazar aparece antes de confirmar.

**Matiz sobre `vinculada`**: el flujo normal (`c1` de [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md), que bloquea el envío si queda cualquier fila `vinculada=False`) garantiza que una `Guia` `Aprobada` por la vía `enviar -> aprobar` tiene **todas** sus `ReferenciaBibliografica` vinculadas -- para ese origen, todas las copias nacen `vinculada=True` de todos modos. [`escalarGuiaAAprobada()`](../escalarGuiaAAprobada/README.md) es el único camino que **bypasea `c1`**: el `DirectorGrado` escala a `Aprobada` sin resolver candidatas, así que una guía escalada puede llevar filas `vinculada=False`. Replicar `vinculada` fila a fila importa **específicamente para orígenes escalados**.

**Guía destino `Aprobada`**: se permite importar y la `Guia` se degrada a `Borrador` -- mismo mecanismo que [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) (`Guia.confirmar_guardado()`), la misma transición `Aprobada -> Borrador` del [diagrama de estados de `Guia`](/RUP/00-modelo-del-dominio/estados-entidades/guia.puml) que dispara el `Profesor` al empezar a corregir.

**Rastro de la operación**: una sola fila de `HistorialCambio` por la importación completa (`campo="bibliografia"`), con el origen identificado en el comentario ("bibliografía importada desde GII / IYA003"). No una fila por referencia -- la operación es atómica. Es el único rastro de que el contenido no lo redactó el profesor destino.

**Relajación acotada de la regla 404-uniforme**: hoy un `Profesor` recibe `404` en toda `Guia` de una `AsignaturaGrado` que no imparte. Para elegir origen necesita leer qué guías aprobadas de hermanas existen y cuántas referencias traen. Se abre exactamente esa lectura -- bibliografía de una `Guia` `Aprobada` de una `AsignaturaGrado` hermana de una suya, a solo efecto de listar y elegir origen. Ninguna otra lectura cross-grado se abre. La previsualización del contenido fila a fila del origen antes de importar (ver las referencias concretas que se traerán) queda **diferida** a un refinamiento posterior: esta primera versión ofrece recuentos, no el detalle.

**`PonderacionEvaluacion` fuera de esta tanda** (decisión de Manuel en el hilo del issue #184): los rangos por `SistemaEvaluacion` del grado destino pueden diferir de los del origen, el copiado no es tan directo -- se aborda en una tanda posterior.

**Guía canónica**: `GII__IYA003` (Programación I) como destino y `GIOI__IYA003` ("Informática", `Aprobada`) como origen -- par hermano real del piloto, no la guía canónica sola, por ser un caso de uso que necesita mostrar dos guías de grados distintos.

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `REFERENCIAS_BIBLIOGRAFICAS_ABIERTO --> REFERENCIAS_BIBLIOGRAFICAS_ABIERTO : importarBibliografiaDeGuiaHermana()`
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catálogo de casos de uso de `Profesor` sobre `ReferenciaBibliografica`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Guia *-- ReferenciaBibliografica` (composición, exclusiva de la `Guia`: importar es copia, no enlace), `(Grado, Asignatura) .. AsignaturaGrado` con `AsignaturaGrado.asignatura_id` (issue #181), hermandad
- [`abrirReferenciasBibliograficas()`](../abrirReferenciasBibliograficas/README.md) -- pantalla desde la que se dispara este caso de uso (self-loop sobre `REFERENCIAS_BIBLIOGRAFICAS_ABIERTO`)
- [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) -- mecanismo de degradado `Aprobada -> Borrador` compartido
- [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md) -- mismo patrón de `<<choice>>` estructural con botón condicional
- [`importarPlanificacionDocenteDeGuiaHermana()`](../importarPlanificacionDocenteDeGuiaHermana/README.md) -- caso de uso gemelo para la planificación docente
- [Issue #184](https://github.com/mmasias/pyCelda/issues/184) -- diseño cerrado con el usuario; [issue #181](https://github.com/mmasias/pyCelda/issues/181) -- la FK que hace posible la hermandad
