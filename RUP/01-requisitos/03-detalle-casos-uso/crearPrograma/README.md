<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/crearPrograma/README.md) / [Diseño](/RUP/03-diseño/casos-uso/crearPrograma/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/crearPrograma/README.md)|[Diseño](/RUP/03-diseño/casos-uso/crearPrograma/README.md)|[Desarrollo](/RUP/04-desarrollo/casos-uso/crearPrograma/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearPrograma/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Formulario|Error (código ya existente)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearPrograma/wireframe.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearPrograma/wireframe-error.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Dar de alta un `Programa` mínimo en el catálogo de una `Facultad`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Primer caso de uso del catálogo que solicita `codigo` en la creación (`Asignatura`/`MetodologiaDocente` también lo tienen, pero en su momento sus `crearX()` no lo pedían -- divergencia histórica de L0/L1, aquí sin corregir retroactivamente). `codigo` es fijo desde el alta: `editarPrograma()` solo permite tocar `nombre`, mismo criterio que `MetodologiaDocente.codigo`.

**Actualización (issue #181, 2026-09-05)**: la divergencia se cerró para `Asignatura` -- [`crearAsignatura()`](/RUP/01-requisitos/03-detalle-casos-uso/crearAsignatura/README.md) exige `codigo` desde entonces, mismo `<<choice>>` de rechazo que este caso de uso. `MetodologiaDocente.codigo` sigue en el régimen antiguo, sin encargo que lo retome.

**Retocado (issue #148, 2026-09-05)**: `codigo` no tenía restricción de unicidad -- permitió un duplicado real en producción (`GIOI` dos veces, distinta `Facultad`). Se añade una rama de rechazo: si el `codigo` introducido ya existe en cualquier `Facultad`, `crearPrograma()` no crea el `Programa` y presenta un mensaje de error, mismo patrón de `<<choice>>` que [`editarPonderacionEvaluacion()`](/RUP/01-requisitos/03-detalle-casos-uso/editarPonderacionEvaluacion/especificacion.puml) (rango superado). El rechazo es global al catálogo, no por `Facultad`: dos `Programa` con el mismo `codigo` en `Facultad` distintas seguirían siendo el mismo error -- `codigo` identifica el Programa, la `Facultad` es dónde se administra, no una partición del espacio de nombres.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROGRAMAS_ABIERTO --> PROGRAMA_ABIERTO : crearPrograma()`
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` sobre `Programa`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa { codigo, estado }`, formalizado en la discussion [#18](https://github.com/mmasias/pyCelda/discussions/18)
- [`editarPonderacionEvaluacion()`](/RUP/01-requisitos/03-detalle-casos-uso/editarPonderacionEvaluacion/README.md) -- precedente del patrón `<<choice>>` con rama de rechazo y wireframe de error.
