<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/abrirAsignatura/README.md) / [Diseño](/RUP/03-diseño/casos-uso/abrirAsignatura/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirAsignatura()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/abrirAsignatura/README.md)|[Diseño](/RUP/03-diseño/casos-uso/abrirAsignatura/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignatura/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Presente en 2+ Programas|Sin ninguna AsignaturaPrograma todavía|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignatura/wireframe.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignatura/wireframe-sinProgramas.svg)|
|<sup>Código fuente: [wireframes.puml](wireframes.puml)</sup>|<sup>mismo fichero, segundo bloque `@startsalt`</sup>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Consultar el detalle de una `Asignatura` concreta|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

**Retocado el wireframe al cerrar la tanda #486/#487/#488/#492 (issue [#496](https://github.com/mmasias/pyCelda/issues/496)), sin tocar la especificación**: el detalle gana la sección "Presente en" -- tabla con cada `AsignaturaPrograma` que instancia esta `Asignatura` del catálogo (`Programa`, `Materia`, `Curso`/`Semestre`, `Carácter`), resuelta vía `filter_by(asignatura_id=...)` (reverse-lookup, precedente directo en `AsignaturaProgramaRepository.listar_hermanas()`) -- issue [#488](https://github.com/mmasias/pyCelda/issues/488). Caso borde de una `Asignatura` sin ninguna `AsignaturaPrograma` todavía (recién creada, "Asignatura Nueva Sin Instanciar" en el segundo bloque `@startsalt`): mensaje explícito ("no está en ningún Programa todavía"), no una tabla vacía ni un error.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `ASIGNATURAS_ABIERTO --> ASIGNATURA_ABIERTO : abrirAsignatura()`
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` sobre `Asignatura`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Asignatura` (nombre, ects, contenido, estado)
- Datos reales: `backend/app/data/seed/asignaturas.json`, guía canónica `GII__IYA003` (discussion #8)
- [Issue #488](https://github.com/mmasias/pyCelda/issues/488) -- origen de la sección "Presente en"
