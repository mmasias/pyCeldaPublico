<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/eliminarMetodologiaDocente/README.md) / [Diseño](/RUP/03-diseño/casos-uso/eliminarMetodologiaDocente/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarMetodologiaDocente()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/eliminarMetodologiaDocente/README.md)|[Diseño](/RUP/03-diseño/casos-uso/eliminarMetodologiaDocente/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarMetodologiaDocente/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Bloqueada (asignada)|Confirmación (sin asignar)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarMetodologiaDocente/wireframe-bloqueada.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarMetodologiaDocente/wireframe-confirmacion.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`, `DirectorPrograma`|
|**Objetivo**|Eliminar una `MetodologiaDocente` del catálogo del `Programa`, siempre que no esté asignada a ninguna `Materia` ni `AsignaturaPrograma`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Borrado físico bloqueado relacionalmente, mismo patrón que [`eliminarCompetencia()`](../eliminarCompetencia/README.md) (issue [#772](https://github.com/mmasias/pyCelda/issues/772)): basta una asignación en cualquiera de los dos niveles de la cascada para bloquear. El mensaje de bloqueo nombra las `Materia` y `AsignaturaPrograma` concretas, en las mismas dos columnas que la Distribución de la ficha. El servidor vuelve a comprobarlo al borrar (409 con los nombres).

Hasta #772 el bloqueo solo miraba las `Materia` y el mensaje era genérico ("en uso en materias del catálogo"), sin nombres. Códigos y textos de los wireframes ilustrativos.

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `METODOLOGIAS_DOCENTES_ABIERTO --> METODOLOGIAS_DOCENTES_ABIERTO : eliminarMetodologiaDocente()`
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `METODOLOGIAS_DOCENTES_ABIERTO --> METODOLOGIAS_DOCENTES_ABIERTO : eliminarMetodologiaDocente()` (misma pantalla conceptual, rutas `/admin/...`)
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Materia o-- MetodologiaDocente` vía `MetodologiaMateria`, `AsignaturaPrograma o-- MetodologiaDocente` (origen de la regla de bloqueo)
- Issue [#772](https://github.com/mmasias/pyCelda/issues/772)
