<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/editarActividadFormativa/README.md) / [Diseño](/RUP/03-diseño/casos-uso/editarActividadFormativa/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarActividadFormativa()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/editarActividadFormativa/README.md)|[Diseño](/RUP/03-diseño/casos-uso/editarActividadFormativa/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarActividadFormativa/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarActividadFormativa/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`, `DirectorPrograma`|
|**Objetivo**|Modificar el código o el nombre de una `ActividadFormativa` del catálogo de un `Programa`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Mismo formulario que [`crearActividadFormativa()`](../crearActividadFormativa/README.md), con los datos actuales y el mismo `<<choice>>` de código repetido dentro del `Programa` (excluida la propia actividad), como [`editarCompetencia()`](../editarCompetencia/README.md) (issue [#772](https://github.com/mmasias/pyCelda/issues/772)). El `codigo` es editable: el catálogo reproduce el de la memoria del programa y corregir un código mal transcrito es un caso real. La actividad no cambia de `Programa`. Editar no toca las horas ni la presencialidad repartidas: las filas de cada `Materia` y `AsignaturaPrograma` apuntan a la actividad, no a su código.

**Histórico**: hasta #772 el `codigo` no era editable una vez creada la actividad y no había `<<choice>>`; el catálogo era de la `Universidad`, solo para `Admin`.

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `ACTIVIDAD_FORMATIVA_ABIERTO --> ACTIVIDAD_FORMATIVA_ABIERTO : editarActividadFormativa()`
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `ACTIVIDAD_FORMATIVA_ABIERTO --> ACTIVIDAD_FORMATIVA_ABIERTO : editarActividadFormativa()` (misma pantalla conceptual, rutas `/admin/...`)
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa *-- ActividadFormativa`, unicidad de `codigo` en el `Programa`
- [`editarCompetencia()`](../editarCompetencia/README.md) -- patrón de origen
