<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirAsignaturasGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturasGrado/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturasGrado/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorGrado`|
|**Objetivo**|Consultar el listado de `AsignaturaGrado` de un `Grado`, con el profesorado que las imparte|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

Propio de `DirectorGrado`, sin equivalente en `Admin`: el `Admin` no tiene un listado plural de `AsignaturaGrado`, accede a ellas desde el atajo plano embebido en [`abrirGrado()`](../abrirGrado/README.md) (retocado en este mismo lote). El `DirectorGrado`, en cambio, sí necesita ver de un vistazo todas las `AsignaturaGrado` de su `Grado` junto con el profesorado asignado (`AsignaturaGrado -- Profesor`, plantilla estable de impartición) -- de ahí el listado propio.

Columna **Profesorado**: dato ya presente en el modelo de dominio, mostrado en modo solo lectura -- la gestión de esa asignación (`asignarProfesorAAsignaturaGrado()`/`desasignarProfesorAsignaturaGrado()`, `Admin`) es de L6, todavía sin construir; no lleva botón propio en este listado.

Sin botón "Crear": `crearAsignaturaGrado()` es exclusivo de `Admin`, no de `DirectorGrado` (ver [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml)), mismo criterio que `abrirMaterias()` (`DirectorGrado` la reutiliza para navegar, pero `crearMateria()` sigue siendo de `Admin`).

Una sola fila real en el wireframe (`Programación I`, GII, curso 1) -- única instancia de `AsignaturaGrado` confirmada en el seed hasta la fecha; no se fabrican filas adicionales por adivinanza.

## Referencias

- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `GRADO_ABIERTO --> ASIGNATURAS_GRADO_ABIERTO : abrirAsignaturasGrado()`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- catálogo de casos de uso de `DirectorGrado` sobre `AsignaturaGrado`
- Modelo del dominio -- `Grado, Asignatura .. AsignaturaGrado`, `AsignaturaGrado -- Profesor`
