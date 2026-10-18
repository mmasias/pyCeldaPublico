<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/abrirActividadesFormativas/README.md) / [Diseño](/RUP/03-diseño/casos-uso/abrirActividadesFormativas/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirActividadesFormativas()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/abrirActividadesFormativas/README.md)|[Diseño](/RUP/03-diseño/casos-uso/abrirActividadesFormativas/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirActividadesFormativas/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirActividadesFormativas/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`, `DirectorPrograma`|
|**Objetivo**|Consultar el catálogo de `ActividadFormativa` de un `Programa`|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

Mismo patrón lista/detalle que [`abrirCompetencias()`](../abrirCompetencias/README.md) (issue [#772](https://github.com/mmasias/pyCelda/issues/772)): `Programa *-- ActividadFormativa`, catálogo propio del programa, con las actividades formativas de su memoria (código y denominación literales). Pestaña **🏋️ Actividades formativas** del programa, en las dos vistas (`/programas/:id/actividades-formativas` y `/admin/programas/:id/actividades-formativas`); misma pantalla para los dos actores. `Admin` actúa sobre cualquier `Programa`; el `DirectorPrograma`, sobre los que dirige.

El listado sigue el orden de alta, que es el mismo de las filas de actividades formativas de cada `Materia` y `AsignaturaPrograma` del programa (y el de la memoria, cuando el catálogo se importa del RUCT). Un programa sin actividades formativas presenta el listado vacío.

**Histórico**: hasta #772 el catálogo era institucional, de la `Universidad` (issue [#655](https://github.com/mmasias/pyCelda/issues/655)), con selector de `Universidad`, solo para `Admin` y con entrada desde el panel de administración (`SISTEMA_DISPONIBLE`). Ese botón del panel desaparece: la entrada es ahora la pestaña del programa (`PROGRAMA_ABIERTO`). Antes de #655 era un seed estático de diez actividades sin CRUD (discussion [#227](https://github.com/mmasias/pyCelda/discussions/227)).

Códigos y nombres de los wireframes ilustrativos (formato de las memorias: `AD` dirigida, `AS` supervisada, `AA` autónoma).

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `PROGRAMA_ABIERTO --> ACTIVIDADES_FORMATIVAS_ABIERTO : abrirActividadesFormativas()`
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROGRAMA_ABIERTO --> ACTIVIDADES_FORMATIVAS_ABIERTO : abrirActividadesFormativas()` (misma pantalla conceptual, rutas `/admin/...`)
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa *-- ActividadFormativa`; [README del modelo del dominio](/RUP/00-modelo-del-dominio/README.md), entrada `ActividadFormativa`
- [`abrirCompetencias()`](../abrirCompetencias/README.md) -- patrón de origen (#761)
- Issue [#772](https://github.com/mmasias/pyCelda/issues/772)
