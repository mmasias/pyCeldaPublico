<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarMateria/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Bloqueada (en uso)|Confirmación (sin uso)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarMateria/wireframe-bloqueada.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarMateria/wireframe-confirmacion.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Eliminar una `Materia` de un `Grado`, siempre que no tenga `AsignaturaGrado` asociadas|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Borrado físico bloqueado relacionalmente, mismo patrón que `eliminarFacultad()`/`eliminarMetodologiaDocente()`: a diferencia de `Asignatura`/`Grado`/`AsignaturaGrado` (borrado lógico vía `estado`), `Materia` no tiene `estado` propio -- vive y muere con el `Grado` que la contiene, así que su borrado es siempre físico. El bloqueo usa `AsignaturaGrado`, no `SistemaEvaluacion`, porque `Materia *-- AsignaturaGrado` es la composición cerrada explícitamente como "sin ventana de orfandad" en el modelo de dominio: el alta de una `AsignaturaGrado` es atómica con su `Materia`, así que una `Materia` con `AsignaturaGrado` no puede desaparecer sin dejar huérfanos. Elección de "Programación"/"Ingeniería del Software" para bloqueada/confirmación es ilustrativa: ambas son materias reales de agrupación de asignaturas de GII, pero qué `AsignaturaGrado` tiene cada una en el catálogo real no está en el seed.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `MATERIAS_ABIERTO --> MATERIAS_ABIERTO : eliminarMateria()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catálogo de casos de uso de `Admin` sobre `Materia`
- Modelo del dominio -- `Materia *-- AsignaturaGrado` (composición sin ventana de orfandad, origen de la regla de bloqueo); README, "Cambiar el reparto de Materia... de un Grado implica un Grado nuevo... ni Materia ni ResultadoAprendizaje necesitan estado propio"
