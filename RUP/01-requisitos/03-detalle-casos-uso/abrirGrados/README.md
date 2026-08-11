<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirGrados()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirGrados/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirGrados/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Consultar el listado de `Grado`s de una `Facultad`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Caso de uso reutilizado por `DirectorGrado` (`DirectorGrado --|> Profesor`) como punto de entrada tras iniciar sesión, con una diferencia de contexto: el listado que ve `Admin` es el de una `Facultad` concreta ya abierta, mientras que `DirectorGrado` ve directamente el listado de los Grados que dirige -- ver [diagramaContextoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml). Una sola especificación, no duplicada.

**Corregido en issue [#50](https://github.com/mmasias/pyCelda/issues/50)**: esta reutilización compartía sin más el mismo wireframe (`GII`/`GIOI`/`GIIAA`, con `[Eliminar]` y `+ Crear Grado`) entre `Admin` (correcto, ve toda la institución) y `DirectorGrado` (incorrecto, solo debería ver los grados que dirige, sin acciones de alta/baja que no tiene) -- mismo patrón exacto que [`abrirAsignaturasGrado()`](../abrirAsignaturasGrado/README.md) (issue [#48](https://github.com/mmasias/pyCelda/issues/48)). Segunda variante, `wireframe-porDirector.svg`: mismo caso de uso, invocado con un parámetro (el director que consulta) -- filtrada a `GII` (sin dato real de qué grados dirige cada director en el seed; un grado real real es suficiente para representar el filtro sin fabricar una asignación inexistente). Extiende a `iniciarSesion()` en el aterrizaje de `DirectorGrado` -- `<<extend>>`, no `<<include>>` (condición `rol == DirectorGrado`, disparada tras validar credenciales; ver [README de `iniciarSesion()`](../iniciarSesion/README.md) para la corrección completa: `<<include>>` es incondicional por definición UML, no encaja con una de tres ramas mutuamente excluyentes). Invocado por `UsuarioNoLogueado`, no por `DirectorGrado` -- el rol específico solo existe tras validar credenciales.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `FACULTAD_ABIERTO --> GRADOS_ABIERTO : abrirGrados()`
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `SESION_CERRADA --> GRADOS_ABIERTO : iniciarSesion()`
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` sobre `Grado`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- reutilización del caso de uso por `DirectorGrado`
- Modelo del dominio -- `Facultad *-d- Grado` (composición: origen de la jerarquía de navegación)
