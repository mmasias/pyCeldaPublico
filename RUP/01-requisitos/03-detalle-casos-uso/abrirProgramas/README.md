<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/abrirProgramas/README.md) / [Diseño](/RUP/03-diseño/casos-uso/abrirProgramas/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirProgramas()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/abrirProgramas/README.md)|[Diseño](/RUP/03-diseño/casos-uso/abrirProgramas/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirProgramas/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirProgramas/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`, `DirectorPrograma`|
|**Objetivo**|Consultar el listado de `Programa`s de una `Facultad`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Caso de uso reutilizado por `DirectorPrograma` (`DirectorPrograma --|> Profesor`) como una de las dos secciones de la pantalla de inicio ([`abrirInicio()`](../abrirInicio/README.md), "Mis programas"), con una diferencia de contexto: el listado que ve `Admin` es el de una `Facultad` concreta ya abierta, mientras que `DirectorPrograma` ve directamente el listado de los Programas que dirige -- ver [diagramaContextoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml). Una sola especificación, no duplicada.

**El endpoint no bloquea a una cuenta que no dirige ningún `Programa`** (discussion [#274](https://github.com/mmasias/pyCelda/discussions/274)): devuelve la lista vacía, no un `403`. `abrirInicio()` lo incluye siempre y presenta la sección "Mis programas" vacía cuando aplica -- simétrico con `abrirAsignaturasPrograma()` (variante `Profesor`), que hace lo mismo con "Mis guías".

**Corregido en issue [#50](https://github.com/mmasias/pyCelda/issues/50)**: esta reutilización compartía sin más el mismo wireframe (`GII`/`GIOI`/`GIIAA`, con `[Eliminar]` y `+ Crear Programa`) entre `Admin` (correcto, ve toda la institución) y `DirectorPrograma` (incorrecto, solo debería ver los programas que dirige, sin acciones de alta/baja que no tiene) -- mismo patrón exacto que [`abrirAsignaturasPrograma()`](../abrirAsignaturasPrograma/README.md) (issue [#48](https://github.com/mmasias/pyCelda/issues/48)). Segunda variante, `wireframe-porDirector.svg`: mismo caso de uso, invocado con un parámetro (el director que consulta) -- filtrada a `GII` (sin dato real de qué programas dirige cada director en el seed; un programa real es suficiente para representar el filtro sin fabricar una asignación inexistente). **Antes extendía a `iniciarSesion()` directamente** (`<<extend>>`, condición `rol == DirectorPrograma`); desde la discussion [#274](https://github.com/mmasias/pyCelda/discussions/274) la incluye [`abrirInicio()`](../abrirInicio/README.md) (`<<include>>`, incondicional -- el hub incorpora siempre las dos secciones, la vacuidad por rol es resultado de datos). `abrirInicio()` es lo que extiende a `iniciarSesion()`, invocado por `UsuarioNoLogueado` -- el rol específico solo existe tras validar credenciales.

**Tres páginas del mockup reutilizan esta carpeta, las tres necesitan override manual**: sin él, el multi-wireframe del script combina ambas variantes en cualquier página no protegida -- regresión real detectada al regenerar tras un cambio no relacionado (las etiquetas de `abrirPonderacionesEvaluacion()`), no en el momento de crear la segunda variante. `admin/abrirProgramas.md` y `directorPrograma/abrirProgramas.md` muestran solo `wireframe.svg` (sin filtro) y `wireframe-porDirector.svg` (filtrada) respectivamente; `directorPrograma/iniciarSesion.md` también apunta a la filtrada.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `FACULTAD_ABIERTO --> PROGRAMAS_ABIERTO : abrirProgramas()`
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `INICIO_ABIERTO --> PROGRAMAS_ABIERTO : abrirProgramas()` (deep link a la pantalla completa); el aterrizaje tras el login es `INICIO_ABIERTO`
- [`abrirInicio()`](../abrirInicio/README.md) -- primitiva que `<<include>>` esta variante como sección "Mis programas"
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` sobre `Programa`
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) -- reutilización del caso de uso por `DirectorPrograma`, incluido por `abrirInicio()`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Facultad *-d- Programa` (composición: origen de la jerarquía de navegación)
