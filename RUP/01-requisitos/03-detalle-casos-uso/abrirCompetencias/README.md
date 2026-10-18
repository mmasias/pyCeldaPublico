<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/abrirCompetencias/README.md) / [Diseño](/RUP/03-diseño/casos-uso/abrirCompetencias/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirCompetencias()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/abrirCompetencias/README.md)|[Diseño](/RUP/03-diseño/casos-uso/abrirCompetencias/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirCompetencias/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirCompetencias/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`, `DirectorPrograma`|
|**Objetivo**|Consultar el catálogo de `Competencia` de un `Programa`|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

Mismo patrón lista/detalle que [`abrirResultadosAprendizaje()`](../abrirResultadosAprendizaje/README.md) (issue [#761](https://github.com/mmasias/pyCelda/issues/761)): `Programa *-- Competencia`, catálogo propio del programa. Pestaña **🧭 Competencias** del programa, tras **🎯 Resultados de aprendizaje**, en las dos vistas (`/programas/:id/competencias` y `/admin/programas/:id/competencias`); misma pantalla para los dos actores.

**Columna "Nº de Asign."**: número de `AsignaturaPrograma` del programa (todas sus materias) que tienen asignada la competencia. Solo informativa: la cobertura no se valida ni bloquea nada (#761, punto 2). Con 0, la celda se presenta con fondo rojo suave (#761, punto 3): aviso visual, sin bloqueo. Un programa de memoria de formato nuevo no tiene competencias: el listado sale vacío y nada más cambia.

Códigos y textos de los wireframes ilustrativos: las competencias reales de cada programa se importarán de las memorias verificadas una vez implementado (#761, decisión 9), no están en el seed.

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `PROGRAMA_ABIERTO --> COMPETENCIAS_ABIERTO : abrirCompetencias()`
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROGRAMA_ABIERTO --> COMPETENCIAS_ABIERTO : abrirCompetencias()` (misma pantalla conceptual, rutas `/admin/...`)
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) y [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- package `Competencia` / `Programa`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa *-- Competencia`
- Issue [#761](https://github.com/mmasias/pyCelda/issues/761) -- decisiones de modelado
