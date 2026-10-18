<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/asociarMetodologiaDocenteAMateria/README.md) / [Diseño](/RUP/03-diseño/casos-uso/asociarMetodologiaDocenteAMateria/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > asociarMetodologiaDocenteAMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/asociarMetodologiaDocenteAMateria/README.md)|[Diseño](/RUP/03-diseño/casos-uso/asociarMetodologiaDocenteAMateria/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAMateria/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAMateria/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorPrograma`, `Admin` (issue [#755](https://github.com/mmasias/pyCelda/issues/755))|
|**Objetivo**|Asociar a una `Materia` una `MetodologiaDocente` del catálogo de su `Programa`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Solo elige una `MetodologiaDocente` del catálogo del `Programa` de la `Materia` -- sin `descripcionPropia` en este formulario, mismo criterio C→U que `crearX()`: el alta de la asociación es mínima, y `descripcionPropia` (vacía por defecto) se gestiona aparte en [`editarAsociacionMetodologiaDocenteMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/editarAsociacionMetodologiaDocenteMateria/README.md). El selector solo ofrece las `MetodologiaDocente` del catálogo del `Programa` de la `Materia` todavía no asociadas a ella (issue [#772](https://github.com/mmasias/pyCelda/issues/772)); hasta #772 ofrecía las habilitadas en el `Programa` de un catálogo institucional de `Universidad`, paso de habilitación que desaparece. Cierre del hueco de diseño de L4 en la discussion [#27](https://github.com/mmasias/pyCelda/discussions/27): el catálogo tenía un único verbo `asociarX()`, se completó con el trío (`asociar`/`desasociar`/`editarAsociacion`) al confirmarse que `descripcionPropia` sí justifica una edición propia, a diferencia de la asociación con `ResultadoAprendizaje`.

**Actor `Admin` (issue [#755](https://github.com/mmasias/pyCelda/issues/755))**: `Admin` gana esta transición con paridad completa respecto a `DirectorPrograma` -- las dos vistas de la materia son espejo en responsabilidades, para que cualquiera de los dos pueda corregir. Misma ficha, mismo wireframe y mismas reglas; es un self-loop de `MATERIA_ABIERTO` también en [diagramaContextoAdmin.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml). Sin alcance por programa: `Admin` actúa sobre cualquier `Materia`. La metodología elegida tiene que ser del mismo `Programa` que la `Materia`, para los dos actores.


## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `MATERIA_ABIERTO --> MATERIA_ABIERTO : asociarMetodologiaDocenteAMateria()`
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) -- catálogo de casos de uso de `DirectorPrograma` sobre `Materia`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa *-- MetodologiaDocente`; `Materia o-- MetodologiaDocente` vía `MetodologiaMateria{descripcionPropia}`
- [Discussion #27](https://github.com/mmasias/pyCelda/discussions/27) -- cierre del hueco de verbos de asociación a nivel de `Materia`
