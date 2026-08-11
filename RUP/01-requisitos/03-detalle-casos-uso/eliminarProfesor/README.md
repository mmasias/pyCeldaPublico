<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarProfesor()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarProfesor/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Bloqueada (asignado o director)|Confirmación (sin vínculos activos)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarProfesor/wireframe-bloqueada.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarProfesor/wireframe-confirmacion.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Eliminar un `Profesor` del catálogo institucional, siempre que no tenga `AsignaturaGrado` asignadas, no sea `DirectorGrado` de ningún `Grado` y no esté referenciado por ninguna `Guia`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

`Profesor` sí se borra físicamente (a diferencia de `Asignatura`/`Grado`/`AsignaturaGrado`, ver [`eliminarAsignatura()`](/RUP/01-requisitos/03-detalle-casos-uso/eliminarAsignatura/README.md)) -- no tiene atributo `estado` en el modelo. Bloqueo con tres condiciones combinadas en el mismo `<<choice>>`, mismo patrón que `eliminarFacultad()`: profesorado asignado (`AsignaturaGrado -- Profesor`), rol activo de `DirectorGrado` (`Grado o- DirectorGrado`) o aparecer referenciado en alguna `Guia` (`Guia -- Profesor`, ver [issue #13](https://github.com/mmasias/pyCelda/issues/13)). Las dos primeras admiten deshacerse con una acción previa de otro caso de uso (`desasignarProfesorAsignaturaGrado()`, `quitarDirectorGrado()`, ninguno detallado todavía); la tercera no -- una `Guia` histórica no se "desasigna", así que un `Profesor` que alguna vez impartió una guía queda permanentemente bloqueado para el borrado físico.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROFESORES_ABIERTO --> PROFESORES_ABIERTO : eliminarProfesor()`
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` sobre `Profesor`
- Modelo del dominio -- `AsignaturaGrado -- Profesor` (profesorado como plantilla estable), `Grado o- DirectorGrado`
