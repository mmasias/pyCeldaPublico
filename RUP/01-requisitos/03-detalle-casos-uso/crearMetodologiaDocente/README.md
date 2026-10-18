<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/crearMetodologiaDocente/README.md) / [Diseño](/RUP/03-diseño/casos-uso/crearMetodologiaDocente/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearMetodologiaDocente()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/crearMetodologiaDocente/README.md)|[Diseño](/RUP/03-diseño/casos-uso/crearMetodologiaDocente/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearMetodologiaDocente/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearMetodologiaDocente/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`, `DirectorPrograma`|
|**Objetivo**|Dar de alta una `MetodologiaDocente` en el catálogo de un `Programa`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Sin patrón C→U, igual que [`crearCompetencia()`](../crearCompetencia/README.md): `código` y `descripción` se piden a la vez porque ambos identifican la metodología desde el alta (los dos literales de la memoria). Diferencias con `Competencia` (issue [#772](https://github.com/mmasias/pyCelda/issues/772)):

- **Sin `tipo`**: la metodología solo tiene código y descripción.
- **Descripción multilínea**, hasta 500 caracteres (código hasta 20).

**`<<choice>>` de código repetido**: `codigo` es único dentro del `Programa`, sin distinguir mayúsculas y minúsculas. Si ya lo usa otra metodología del programa, el sistema presenta el mensaje y el formulario sigue con lo escrito. El mismo código en otro `Programa` sí se admite: cada memoria numera las suyas.

La salida lleva a la ficha de la metodología creada (`<<include>>` de `editarMetodologiaDocente()`, nota obligatoria de la transición de salida). Hasta #772 el alta era solo del `Admin`, en el catálogo institucional de una `Universidad` elegida en el formulario, sin control de código repetido.

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `METODOLOGIAS_DOCENTES_ABIERTO --> METODOLOGIA_DOCENTE_ABIERTO : crearMetodologiaDocente()`
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `METODOLOGIAS_DOCENTES_ABIERTO --> METODOLOGIA_DOCENTE_ABIERTO : crearMetodologiaDocente()` (misma pantalla conceptual, rutas `/admin/...`)
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa *-- MetodologiaDocente`; [README del modelo del dominio](/RUP/00-modelo-del-dominio/README.md), unicidad de `codigo` dentro del `Programa`
- Issue [#772](https://github.com/mmasias/pyCelda/issues/772)
