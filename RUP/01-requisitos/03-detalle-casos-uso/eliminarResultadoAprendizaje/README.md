<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/eliminarResultadoAprendizaje/README.md) / [Diseño](/RUP/03-diseño/casos-uso/eliminarResultadoAprendizaje/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarResultadoAprendizaje()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/eliminarResultadoAprendizaje/README.md)|[Diseño](/RUP/03-diseño/casos-uso/eliminarResultadoAprendizaje/README.md)|[Desarrollo](/RUP/04-desarrollo/casos-uso/eliminarResultadoAprendizaje/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarResultadoAprendizaje/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Bloqueada (en uso)|Confirmación (sin uso)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarResultadoAprendizaje/wireframe-bloqueada.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarResultadoAprendizaje/wireframe-confirmacion.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`, `DirectorPrograma`|
|**Objetivo**|Eliminar un `ResultadoAprendizaje` del catálogo del `Programa`, siempre que no esté asignado a ninguna `Materia` ni `AsignaturaPrograma`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Borrado físico bloqueado relacionalmente, mismo patrón que `eliminarFacultad()`/`eliminarMetodologiaDocente()`/`eliminarMateria()`: `ResultadoAprendizaje` no tiene `estado` propio, igual que `Materia` -- vive y muere con el `Programa` que lo contiene. El bloqueo cubre los dos niveles de la cascada de asignación (`Materia o-- ResultadoAprendizaje`, `AsignaturaPrograma o-- ResultadoAprendizaje`): basta con una asignación en cualquiera de los dos para bloquear, ningún RA llega a una `AsignaturaPrograma` sin pasar antes por su `Materia`. RAC2/RAH2 son datos reales del plan de estudios de GII, aportados por el usuario en la [issue #23](https://github.com/mmasias/pyCelda/issues/23); elección de cuál está bloqueado/libre es ilustrativa, no una afirmación sobre asignaciones reales (esa asignación concreta es L4, sin empezar).

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `RESULTADOS_APRENDIZAJE_ABIERTO --> RESULTADOS_APRENDIZAJE_ABIERTO : eliminarResultadoAprendizaje()`
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `RESULTADOS_APRENDIZAJE_ABIERTO --> RESULTADOS_APRENDIZAJE_ABIERTO : eliminarResultadoAprendizaje()` (compartido con `Admin` desde el issue [#642](https://github.com/mmasias/pyCelda/issues/642); pantalla propia en `/admin/...`, `*Admin.tsx`)
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) -- catálogo de casos de uso de `DirectorPrograma` sobre `ResultadoAprendizaje`
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` (incluye este caso de uso desde el issue [#642](https://github.com/mmasias/pyCelda/issues/642))
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Materia o-- ResultadoAprendizaje`, `AsignaturaPrograma o-- ResultadoAprendizaje` (origen de la regla de bloqueo, cascada en dos pasos)
