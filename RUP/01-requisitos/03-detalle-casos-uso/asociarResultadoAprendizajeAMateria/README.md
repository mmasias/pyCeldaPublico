<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/asociarResultadoAprendizajeAMateria/README.md) / [Diseño](/RUP/03-diseño/casos-uso/asociarResultadoAprendizajeAMateria/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > asociarResultadoAprendizajeAMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/asociarResultadoAprendizajeAMateria/README.md)|[Diseño](/RUP/03-diseño/casos-uso/asociarResultadoAprendizajeAMateria/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAMateria/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAMateria/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorPrograma`, `Admin` (issue [#755](https://github.com/mmasias/pyCelda/issues/755))|
|**Objetivo**|Asociar un `ResultadoAprendizaje` del catálogo del `Programa` a una `Materia`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Primer escalón de la cascada `Programa`->`Materia`->`AsignaturaPrograma`. A diferencia de `asociarMetodologiaDocenteAMateria()`, aquí no hace falta un `editarAsociacionX()`: `Materia o-u- ResultadoAprendizaje` es agregación simple, sin clase de asociación ni atributo propio que editar -- el trío se queda en par (`asociar`/`desasociar`), cerrado así en la discussion [#27](https://github.com/mmasias/pyCelda/discussions/27). El selector solo ofrece `ResultadoAprendizaje` del `Programa` todavía no asociados a esta `Materia`. RAK2 es dato real (issue [#23](https://github.com/mmasias/pyCelda/issues/23)); qué `ResultadoAprendizaje` concretos usa "Programación" es ilustrativo.

**Actor `Admin` (issue [#755](https://github.com/mmasias/pyCelda/issues/755))**: `Admin` gana esta transición con paridad completa respecto a `DirectorPrograma` -- las dos vistas de la materia son espejo en responsabilidades, para que cualquiera de los dos pueda corregir. Misma ficha, mismo wireframe y mismas reglas; es un self-loop de `MATERIA_ABIERTO` también en [diagramaContextoAdmin.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml). Sin alcance por programa: `Admin` actúa sobre cualquier `Materia`.


**Texto del selector (v0.11.27)**: cada opción muestra `código -- extracto` de la descripción (unos 80 caracteres, cortado en un espacio, con "..."; `extractoResultado()` en `frontend/src/resultadoAprendizaje.ts`, común a materia y asignatura, Director y Admin), y bajo el selector se ve el texto completo del elegido. Las descripciones van de unos pocos caracteres a varios miles: ni la descripción entera ni el `tipo` (todos `General`) servían para elegir.

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `MATERIA_ABIERTO --> MATERIA_ABIERTO : asociarResultadoAprendizajeAMateria()`
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) -- catálogo de casos de uso de `DirectorPrograma` sobre `Materia`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Materia o-u- ResultadoAprendizaje`, README: "el director asigna primero a cada `Materia` un subconjunto del catálogo de `ResultadoAprendizaje` del `Programa`"
- [Discussion #27](https://github.com/mmasias/pyCelda/discussions/27) -- cierre del hueco de verbos de asociación a nivel de `Materia`
