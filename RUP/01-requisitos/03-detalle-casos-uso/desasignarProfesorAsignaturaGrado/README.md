<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > desasignarProfesorAsignaturaGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasignarProfesorAsignaturaGrado/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Normal (queda otro Profesor)|Advertencia (se queda sin ninguno)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasignarProfesorAsignaturaGrado/wireframe-normal.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasignarProfesorAsignaturaGrado/wireframe-advertencia.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Desasignar un `Profesor` de una `AsignaturaGrado`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

**Sin `<<choice>>` bloqueante, a diferencia de `quitarDirectorGrado()`/`desasociarMetodologiaDocenteMateria()`/`desasociarResultadoAprendizajeAMateria()`**: `AsignaturaGrado` es el último escalón de la cascada de reparto -- no hay un nivel estructural inferior que dependa de este profesorado para bloquear la desasignación. Tampoco hay invariante de mínimo (a diferencia de `Grado`-`DirectorGrado`, que exige al menos un director).

Confirmación con advertencia condicional, no bloqueo: si el `Profesor` que se desasigna es el único de esa `AsignaturaGrado`, el sistema lo advierte -- la guía docente que se genere sobre ella podría quedar incompleta -- pero permite confirmar igual, para cubrir el caso real de mantenimiento en que se están reconstruyendo las asignaciones. Cierre en la discussion [#33](https://github.com/mmasias/pyCelda/discussions/33), que también apunta como pendiente futuro (fuera de alcance de L6, depende de `Guia`/`PonderacionEvaluacion`) una validación de completitud antes de `generarGuiasPDF()`.

**Efecto colateral sobre el ciclo de vida de `Guia` (issue [#254](https://github.com/mmasias/pyCelda/issues/254))**: mismo que `asignarProfesorAAsignaturaGrado()`. Este caso de uso nunca tocó `Guia -- Profesor` y sigue sin tocarlo. Lo nuevo: si la desasignación cambia la plantilla y la `Guia` activa está `Aprobada`, pasa a `EnRevision` + fila de `HistorialCambio` (`autor` centinela `0`, `comentario="En revisión por cambio en los profesores que la imparten"`) para que el `DirectorGrado` re-apruebe; al re-aprobar, `Guia -- Profesor` se re-deriva de la plantilla y el profesor desasignado sale de la copia. En cualquier otro estado de la `Guia`, nada más. Ver el detalle del mecanismo en [`asignarProfesorAAsignaturaGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/asignarProfesorAAsignaturaGrado/README.md) y el [modelo del dominio](/RUP/00-modelo-del-dominio/README.md).

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `ASIGNATURA_GRADO_ABIERTO --> ASIGNATURA_GRADO_ABIERTO : desasignarProfesorAsignaturaGrado()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catálogo de casos de uso de `Admin` sobre `AsignaturaGrado`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaGrado -- Profesor`; README, `Guia -- Profesor` re-derivada al aprobar (issue #254)
- [Issue #254](https://github.com/mmasias/pyCelda/issues/254) / [discussion #255](https://github.com/mmasias/pyCelda/discussions/255) -- efecto colateral `Aprobada -> EnRevision` al cambiar la plantilla
- [Discussion #33](https://github.com/mmasias/pyCelda/discussions/33) -- cierre del `<<choice>>` (sin bloqueo, con advertencia condicional) y retiro de `editarAsignacionProfesorAsignaturaGrado()` del catálogo
- [`asignarProfesorAAsignaturaGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/asignarProfesorAAsignaturaGrado/README.md) -- caso de uso complementario (alta de la asignación)
