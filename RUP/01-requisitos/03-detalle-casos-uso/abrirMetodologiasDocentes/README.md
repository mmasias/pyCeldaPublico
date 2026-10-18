<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/abrirMetodologiasDocentes/README.md) / [Diseño](/RUP/03-diseño/casos-uso/abrirMetodologiasDocentes/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirMetodologiasDocentes()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/abrirMetodologiasDocentes/README.md)|[Diseño](/RUP/03-diseño/casos-uso/abrirMetodologiasDocentes/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiasDocentes/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiasDocentes/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`, `DirectorPrograma`|
|**Objetivo**|Consultar el catálogo de `MetodologiaDocente` de un `Programa`|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

Mismo patrón lista/detalle que [`abrirCompetencias()`](../abrirCompetencias/README.md) (issue [#772](https://github.com/mmasias/pyCelda/issues/772)): `Programa *-- MetodologiaDocente`, catálogo propio del programa con el código y la descripción literales de su memoria verificada. Pestaña **🧩 Metodologías** del programa, tras **🧭 Competencias**, en las dos vistas (`/programas/:id/metodologias-docentes` y `/admin/programas/:id/metodologias-docentes`); misma pantalla para los dos actores. Sin columna de tipo: la metodología solo tiene código y descripción.

**Columna "Nº de Asign."**: número de `AsignaturaPrograma` del programa (todas sus materias) que tienen asignada la metodología. Solo informativa, como en `Competencia`: con 0, la celda se presenta con fondo rojo suave, sin bloqueo. Un programa sin metodologías presenta el aviso "Este programa no tiene metodologías docentes." en lugar de la tabla.

**Absorbe a `abrirMetodologiasDocentesPrograma()`**: hasta #772 había dos listados, el catálogo institucional de la `Universidad` (este caso de uso, con selector de `Universidad`, solo `Admin`, desde `SISTEMA_DISPONIBLE`) y el subconjunto habilitado en cada `Programa` (`abrirMetodologiasDocentesPrograma()`, con `asociarMetodologiaDocenteAPrograma()`/`desasociarMetodologiaDocentePrograma()`, issues [#526](https://github.com/mmasias/pyCelda/issues/526)/[#527](https://github.com/mmasias/pyCelda/issues/527)). Con el catálogo en el `Programa` el paso de habilitación desaparece y queda un único listado, dentro del programa.

Códigos y textos de los wireframes ilustrativos: cada programa tiene los de su memoria (en las memorias, el mismo código MD2 puede significar cosas distintas según el programa).

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `PROGRAMA_ABIERTO --> METODOLOGIAS_DOCENTES_ABIERTO : abrirMetodologiasDocentes()`
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROGRAMA_ABIERTO --> METODOLOGIAS_DOCENTES_ABIERTO : abrirMetodologiasDocentes()` (misma pantalla conceptual, rutas `/admin/...`)
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) y [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- package `MetodologiaDocente`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa *-- MetodologiaDocente`
- Issue [#772](https://github.com/mmasias/pyCelda/issues/772) -- catálogo por programa
