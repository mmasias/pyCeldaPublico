<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/abrirMetodologiasDocentesPrograma/README.md) / [Diseño](/RUP/03-diseño/casos-uso/abrirMetodologiasDocentesPrograma/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirMetodologiasDocentesPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/abrirMetodologiasDocentesPrograma/README.md)|[Diseño](/RUP/03-diseño/casos-uso/abrirMetodologiasDocentesPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiasDocentesPrograma/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiasDocentesPrograma/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`, `DirectorPrograma`|
|**Objetivo**|Consultar las `MetodologiaDocente` asociadas a un `Programa` y gestionar esa asociación|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

Pantalla propia del lado `DirectorPrograma` (issue [#638](https://github.com/mmasias/pyCelda/issues/638), corrección sobre [#636](https://github.com/mmasias/pyCelda/issues/636)): sigue el patrón de `abrirResultadosAprendizaje()` (página colgada de `NavPrograma`) en lugar de una sección embebida en `abrirPrograma()`. Caso de uso compartido `Admin`, `DirectorPrograma` desde el issue [#640](https://github.com/mmasias/pyCelda/issues/640), igual que `abrirMaterias()`: cada actor con su propia pantalla (`/admin/programas/:id/metodologias-docentes`, `MetodologiasDocentesProgramaAdmin.tsx`, calcada de `MateriasAdmin.tsx` con un único "Volver" y sin menú persistente / `/programas/:id/metodologias-docentes` para el Director).

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROGRAMA_ABIERTO --> METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO : abrirMetodologiasDocentesPrograma()` (nombre distinto del `METODOLOGIAS_DOCENTES_ABIERTO` del catálogo institucional global de `MetodologiaDocente` -- misma palabra, pantallas y rutas distintas)
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `PROGRAMA_ABIERTO --> METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO : abrirMetodologiasDocentesPrograma()`
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) y [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogos de casos de uso sobre `MetodologiaDocente`
- [`asociarMetodologiaDocenteAPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAPrograma/README.md) y [`desasociarMetodologiaDocentePrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocentePrograma/README.md) -- acciones disponibles desde esta pantalla (self-loop sobre `METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO` en ambos diagramas, Director y Admin).

**Tabla Código/Descripción**: catálogo de asociación, no CRUD de la propia `MetodologiaDocente` (sin columna "Asignaturas" ni "Eliminar").
