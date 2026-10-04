<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/definirDirectorPrograma/README.md) / [Diseño](/RUP/03-diseño/casos-uso/definirDirectorPrograma/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > definirDirectorPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/definirDirectorPrograma/README.md)|[Diseño](/RUP/03-diseño/casos-uso/definirDirectorPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/definirDirectorPrograma/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Desde el Profesor|Desde el Programa (issue #492)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/definirDirectorPrograma/wireframe.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/definirDirectorPrograma/wireframe-desdePrograma.svg)|
|<sup>Código fuente: [wireframes.puml](wireframes.puml)</sup>|<sup>mismo fichero, segundo bloque `@startsalt`</sup>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Nombrar a un `Profesor` como `DirectorPrograma` de un `Programa` concreto|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

`DirectorPrograma` no es una entidad propia sino un rol sobre un `Profesor` ya abierto (`PROFESOR_ABIERTO`) -- originalmente el flujo empezaba solo desde el Profesor, con selector de Programa (decisión cerrada en la discussion [#18](https://github.com/mmasias/pyCelda/discussions/18), que entonces descartó el flujo inverso desde el Programa como "extensión trivial futura"). Cardinalidad `Programa`-`DirectorPrograma` muchos a muchos: **asignación libre, sin `<<choice>>`** en ambas entradas -- un Programa admite varios directores simultáneos (cubre la figura del coordinador) y un Profesor puede dirigir varios Programas a la vez, así que no hay ninguna exclusión que validar más allá de no repetir una asignación ya existente.

**Segunda entrada desde `PROGRAMA_ABIERTO`, issue [#492](https://github.com/mmasias/pyCelda/issues/492)** -- la "extensión trivial futura" que la discussion #18 dejó pendiente: **flujo alternativo del mismo caso de uso**, no uno nuevo (mismo objetivo de actor -- nombrar un `Profesor` director de un `Programa` --, misma postcondición, mismo endpoint `POST /profesores/{profesor_id}/directores-programa`). Lo único que cambia es qué dato ya se conoce de antemano y cuál hay que seleccionar: desde el Profesor se selecciona el Programa (selector excluye los que ya dirige); desde el Programa se selecciona el Profesor (selector nuevo, `GET /admin/programas/{programa_id}/profesores-disponibles-para-dirigir`, reverso exacto del que ya existía). Sin pantalla propia en la nueva entrada: `ProgramaAdmin.tsx` la resuelve inline en la propia portada del Programa (ver retoque de [`abrirPrograma()`](../abrirPrograma/README.md)), a diferencia de la entrada desde el Profesor que sí navega a una pantalla dedicada (`DefinirDirectorPrograma.tsx`).

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROFESOR_ABIERTO --> PROFESOR_ABIERTO : definirDirectorPrograma()`, y ahora también `PROGRAMA_ABIERTO --> PROGRAMA_ABIERTO : definirDirectorPrograma()` (issue #492)
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` sobre `Profesor` (sin cambio: flujo alternativo, no entrada nueva de catálogo)
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa o- DirectorPrograma` (agregación, muchos a muchos)
- [Discussion #18](https://github.com/mmasias/pyCelda/discussions/18) -- cierre original de flujo, cardinalidad y ausencia de `<<choice>>`; apuntaba el flujo inverso ahora resuelto por el #492
- [`quitarDirectorPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/quitarDirectorPrograma/README.md) -- caso de uso complementario (baja del rol), misma segunda entrada
- [`abrirPrograma()`](../abrirPrograma/README.md) -- portada donde vive la sección "Directores" que hospeda esta segunda entrada
- [Issue #492](https://github.com/mmasias/pyCelda/issues/492) -- origen de la segunda entrada
