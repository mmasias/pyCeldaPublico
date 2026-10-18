<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/crearActividadFormativa/README.md) / [Diseño](/RUP/03-diseño/casos-uso/crearActividadFormativa/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearActividadFormativa()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/crearActividadFormativa/README.md)|[Diseño](/RUP/03-diseño/casos-uso/crearActividadFormativa/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearActividadFormativa/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearActividadFormativa/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`, `DirectorPrograma`|
|**Objetivo**|Dar de alta una `ActividadFormativa` en el catálogo de un `Programa`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Sin patrón C→U, como [`crearCompetencia()`](../crearCompetencia/README.md): `codigo` y `nombre` se piden a la vez porque los dos identifican la actividad desde el alta (issue [#772](https://github.com/mmasias/pyCelda/issues/772)).

- **`<<choice>>` de código repetido**: `codigo` es único dentro del `Programa`, sin distinguir mayúsculas. Si ya lo usa otra actividad formativa del programa, el sistema presenta el mensaje y el formulario sigue con lo escrito. El mismo código en otro `Programa` es válido: cada programa tiene el catálogo de su memoria.
- **Invariante de autopoblado**: cada `Materia` y cada `AsignaturaPrograma` del `Programa` tiene siempre una fila por cada actividad del catálogo. Al crear la actividad, el sistema añade su fila a 0 horas (y, en la `Materia`, a 0 % de presencialidad) en todas las ya existentes del programa. Las horas se reparten después, desde [`editarActividadesFormativasMateria()`](../editarActividadesFormativasMateria/README.md) y [`editarActividadesFormativasAsignaturaPrograma()`](../editarActividadesFormativasAsignaturaPrograma/README.md).

La salida lleva a la ficha de la actividad creada (nota `editarActividadFormativa()` de la transición de salida: la edición disponible desde la ficha).

**Histórico**: hasta #772 la actividad nacía en el catálogo institucional de una `Universidad` elegida en el formulario (issue [#655](https://github.com/mmasias/pyCelda/issues/655)), solo por `Admin` y sin control de código repetido.

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `ACTIVIDADES_FORMATIVAS_ABIERTO --> ACTIVIDAD_FORMATIVA_ABIERTO : crearActividadFormativa()`
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `ACTIVIDADES_FORMATIVAS_ABIERTO --> ACTIVIDAD_FORMATIVA_ABIERTO : crearActividadFormativa()` (misma pantalla conceptual, rutas `/admin/...`)
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa *-- ActividadFormativa`; [README del modelo del dominio](/RUP/00-modelo-del-dominio/README.md), invariante de autopoblado
- [`crearCompetencia()`](../crearCompetencia/README.md) -- patrón de origen
- Issue [#772](https://github.com/mmasias/pyCelda/issues/772)
