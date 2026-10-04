<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/asignarProfesorAAsignaturaPrograma/README.md) / [Diseño](/RUP/03-diseño/casos-uso/asignarProfesorAAsignaturaPrograma/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > asignarProfesorAAsignaturaPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/asignarProfesorAAsignaturaPrograma/README.md)|[Diseño](/RUP/03-diseño/casos-uso/asignarProfesorAAsignaturaPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/asignarProfesorAAsignaturaPrograma/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/asignarProfesorAAsignaturaPrograma/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Asignar un `Profesor` como impartidor de una `AsignaturaPrograma` concreta|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

`AsignaturaPrograma -- Profesor` (ver [modelo del dominio](/RUP/00-modelo-del-dominio/README.md)) es la plantilla estable de impartición: gestionada por `Admin`, no cambia cada curso académico y admite varios profesores por `AsignaturaPrograma`. Asignación libre, sin `<<choice>>` -- no hay ninguna exclusión que validar, mismo patrón que `asociarMetodologiaDocenteAMateria()`/`definirDirectorPrograma()`. El selector solo excluye los `Profesor` ya asignados a esta `AsignaturaPrograma`, por no tener sentido repetir la asignación.

**Exclusivo de `Admin`, no de `DirectorPrograma`**: este no es un sistema de gestión de personal docente, es un sistema de gestión de guías docentes -- el director ve el profesorado asignado (`abrirAsignaturasPrograma()`/`abrirAsignaturaPrograma()`, ambos de solo lectura para él), pero no lo gestiona. Cierre en la discussion [#33](https://github.com/mmasias/pyCelda/discussions/33).

**Efecto colateral sobre el ciclo de vida de `Guia` (issue [#254](https://github.com/mmasias/pyCelda/issues/254), cierre de diseño en la discussion [#255](https://github.com/mmasias/pyCelda/discussions/255))**: este caso de uso **ya no toca `Guia -- Profesor` directamente**. Si la asignación cambia de verdad la plantilla (asignar un `Profesor` ya asignado es no-op y no dispara nada) y la `Guia` activa de esa `AsignaturaPrograma` está `Aprobada`, el sistema la pasa a `EnRevision` -- transición administrativa nueva, sin re-ejecutar las reglas `c1`/`c2`/`c3` de `enviarGuiaARevision()` -- y registra una fila de `HistorialCambio` (`campo="estado"`, `valorAnterior="Aprobada"`, `valorNuevo="EnRevision"`, `autor` centinela `0`, `comentario="En revisión por cambio en los profesores que la imparten"`). En cualquier otro estado de la `Guia` no se hace nada más: la gestión de profesores es transparente para el `DirectorPrograma` y la próxima aprobación sincroniza `Guia -- Profesor` con la plantilla sola (`Guia.aprobar()` re-deriva la copia, ver [modelo del dominio](/RUP/00-modelo-del-dominio/README.md)). La re-aprobación del director es un clic (`aprobarGuia()` aprueba desde el estado que sea). Un banner en la guía -- mismo patrón que `comentario_rechazo` -- explica al director por qué volvió a revisión.

## Notas de diseño y trazabilidad

- Retirado de la nota de la especificación (detalle técnico): si la plantilla cambia de verdad y la `Guia` activa está `Aprobada`, pasa a `EnRevision` con una fila de `HistorialCambio` (autor centinela); al aprobar, `Guia--Profesor` se re-deriva de la plantilla (issue [#254](https://github.com/mmasias/pyCelda/issues/254)). En cualquier otro estado, nada más. Detalle completo en la sección de efecto colateral anterior.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `ASIGNATURA_PROGRAMA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO : asignarProfesorAAsignaturaPrograma()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catálogo de casos de uso de `Admin` sobre `AsignaturaPrograma`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaPrograma -- Profesor` (plantilla estable, muchos a muchos)
- [Discussion #33](https://github.com/mmasias/pyCelda/discussions/33) -- cierre del recuento de L6, confirma el par asignar/desasignar (sin `editarAsignacion`, sin atributo propio en la relación)
- [Discussion #47](https://github.com/mmasias/pyCelda/discussions/47) -- planificación de Análisis; origen del hallazgo del efecto colateral sobre `Guia -- Profesor` (mecanismo sustituido por el de #254)
- [Issue #254](https://github.com/mmasias/pyCelda/issues/254) / [discussion #255](https://github.com/mmasias/pyCelda/discussions/255) -- `Guia -- Profesor` pasa a re-derivarse al aprobar; este caso de uso deja de tocarlo y gana el efecto colateral `Aprobada -> EnRevision`
- [`aprobarGuia()`](/RUP/01-requisitos/03-detalle-casos-uso/aprobarGuia/README.md) -- re-deriva `Guia -- Profesor` de la plantilla al pasar a `Aprobada`
- [`activarCursoAcademico()`](/RUP/01-requisitos/03-detalle-casos-uso/activarCursoAcademico/README.md) -- crea la `Guia` (con o sin `Profesor`) cuyo profesorado este caso de uso puede terminar mandando a re-revisión
- [`desasignarProfesorAsignaturaPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/desasignarProfesorAsignaturaPrograma/README.md) -- caso de uso complementario (baja de la asignación), mismo efecto colateral
