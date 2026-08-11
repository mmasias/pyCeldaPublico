<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

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

**Sin `<<choice>>` bloqueante, a diferencia de `quitarDirectorGrado()`/`desasociarMetodologiaDocenteMateria()`/`desasociarResultadoAprendizajeAMateria()`**: `AsignaturaGrado` es el último escalón de la cascada de reparto -- no hay un nivel estructural inferior que dependa de este profesorado para bloquear la desasignación, y el modelo de dominio cierra que `Guia -- Profesor` se copia puntualmente al crear la `Guia` (clonado al abrir el curso), no se deriva en vivo de `AsignaturaGrado -- Profesor` -- así que desasignar aquí no rompe ninguna `Guia` ya creada. Tampoco hay invariante de mínimo (a diferencia de `Grado`-`DirectorGrado`, que exige al menos un director).

Confirmación con advertencia condicional, no bloqueo: si el `Profesor` que se desasigna es el único de esa `AsignaturaGrado`, el sistema lo advierte -- la guía docente que se genere sobre ella podría quedar incompleta -- pero permite confirmar igual, para cubrir el caso real de mantenimiento en que se están reconstruyendo las asignaciones. Cierre en la discussion [#33](https://github.com/mmasias/pyCelda/discussions/33), que también apunta como pendiente futuro (fuera de alcance de L6, depende de `Guia`/`PonderacionEvaluacion`) una validación de completitud antes de `generarGuiasPDF()`.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `ASIGNATURA_GRADO_ABIERTO --> ASIGNATURA_GRADO_ABIERTO : desasignarProfesorAsignaturaGrado()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catálogo de casos de uso de `Admin` sobre `AsignaturaGrado`
- Modelo del dominio -- `AsignaturaGrado -- Profesor`; README, `Guia -- Profesor` como copia puntual al crear, no derivación en vivo
- [Discussion #33](https://github.com/mmasias/pyCelda/discussions/33) -- cierre del `<<choice>>` (sin bloqueo, con advertencia condicional) y retiro de `editarAsignacionProfesorAsignaturaGrado()` del catálogo
- [`asignarProfesorAAsignaturaGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/asignarProfesorAAsignaturaGrado/README.md) -- caso de uso complementario (alta de la asignación)
