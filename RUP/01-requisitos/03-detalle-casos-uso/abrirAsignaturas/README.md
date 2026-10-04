<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/abrirAsignaturas/README.md) / [Diseño](/RUP/03-diseño/casos-uso/abrirAsignaturas/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirAsignaturas()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/abrirAsignaturas/README.md)|[Diseño](/RUP/03-diseño/casos-uso/abrirAsignaturas/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturas/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturas/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Consultar el listado de `Asignatura` del catálogo institucional|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

**Retocado el wireframe al cerrar la tanda #486/#487/#488/#492 (issue [#496](https://github.com/mmasias/pyCelda/issues/496)), sin tocar la especificación**: el listado gana la columna "Código" (`AsignaturaResponse.codigo`, ya expuesto por el backend, sin endpoint nuevo -- issue [#486](https://github.com/mmasias/pyCelda/issues/486)). Caso borde de `codigo` nulo (asignaturas legacy sin código) reflejado en el wireframe con una fila propia, texto explicativo en vez de "null".

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SISTEMA_DISPONIBLE --> ASIGNATURAS_ABIERTO : abrirAsignaturas()`
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` sobre `Asignatura`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Asignatura` (nombre, ects, contenido, estado), catálogo independiente reutilizado por `AsignaturaPrograma`
- Datos reales: `backend/app/data/seed/asignaturas.json` (repo privado)
- [Issue #486](https://github.com/mmasias/pyCelda/issues/486) -- origen de la columna "Código"
