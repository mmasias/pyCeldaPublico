<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > editarAsignaturaGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarAsignaturaGrado/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarAsignaturaGrado/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorGrado`|
|**Objetivo**|Modificar los datos de una `AsignaturaGrado` de su `Grado`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

**Único caso de edición del catálogo, y no es de `Admin`**: `Admin` crea, abre y elimina `AsignaturaGrado` (ver [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml)), pero no tiene `editarAsignaturaGrado()` propio -- es exclusivo de `DirectorGrado` (ver [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml)). Edita los 7 atributos propios de una vez, sin distinguir en el formulario entre los de identidad (`curso`, `carácter`, `idioma`, `semestre por defecto`) y los de override (`nombre`, `ects`, `contenido`) -- esa distinción sí importa en [`crearAsignaturaGrado()`](../crearAsignaturaGrado/README.md) (dónde hay valor heredado que mostrar de partida), no aquí, donde todos los campos ya tienen un valor propio que mostrar.

**Pendiente, no bloquea este lote**: el modelo del dominio señala `semestreDefault` como invariante una vez que alguna `Guia` se ha creado apoyándose en él -- no antes. Modelar ese bloqueo con un `<<choice>>` (mismo patrón que `editarCursoAcademico()`) requiere la entidad `Guia`, todavía sin construir (L7-L9). Hasta entonces, `semestreDefault` se trata aquí como cualquier otro campo editable; revisar este caso de uso al cerrar L7-L9.

## Referencias

- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `ASIGNATURA_GRADO_ABIERTO --> ASIGNATURA_GRADO_ABIERTO : editarAsignaturaGrado()`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- catálogo de casos de uso de `DirectorGrado` sobre `AsignaturaGrado`
- Modelo del dominio -- `AsignaturaGrado{nombre, curso, caracter, idioma, ects, semestreDefault, contenido, estado}`; README, herencia de `nombre`/`ects`/`contenido`, invarianza condicional de `semestreDefault`
