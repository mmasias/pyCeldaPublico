<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/abrirMetodologiaDocente/README.md) / [Diseño](/RUP/03-diseño/casos-uso/abrirMetodologiaDocente/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirMetodologiaDocente()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/abrirMetodologiaDocente/README.md)|[Diseño](/RUP/03-diseño/casos-uso/abrirMetodologiaDocente/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiaDocente/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiaDocente/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`, `DirectorPrograma`|
|**Objetivo**|Consultar el detalle de una `MetodologiaDocente` y su distribución en materias y asignaturas|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

Ficha de la metodología con su **Distribución**: las `Materia` y las `AsignaturaPrograma` del programa que la tienen asignada, en dos columnas y con enlace a cada una -- mismo diseño que la ficha de [`Competencia`](../abrirCompetencia/README.md) (issue [#772](https://github.com/mmasias/pyCelda/issues/772)). Sin "Código" en el cuerpo: va en la miga (**🧩 Metodologías docentes › MD3**). Sin asignaciones, la Distribución se sustituye por el aviso "Sin asignaciones a materias ni a asignaturas del programa."

La descripción es la del catálogo del `Programa`; la `descripcionPropia` que una `Materia` pueda fijar en su asociación ([`editarAsociacionMetodologiaDocenteMateria()`](../editarAsociacionMetodologiaDocenteMateria/README.md)) no se muestra aquí.

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `METODOLOGIAS_DOCENTES_ABIERTO --> METODOLOGIA_DOCENTE_ABIERTO : abrirMetodologiaDocente()`
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `METODOLOGIAS_DOCENTES_ABIERTO --> METODOLOGIA_DOCENTE_ABIERTO : abrirMetodologiaDocente()` (misma pantalla conceptual, rutas `/admin/...`)
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `MetodologiaDocente{codigo, descripcion}`, `Programa *-- MetodologiaDocente`
- Issue [#772](https://github.com/mmasias/pyCelda/issues/772)
