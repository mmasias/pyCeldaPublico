<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/asociarMetodologiaDocenteAAsignaturaPrograma/README.md) / [Diseño](/RUP/03-diseño/casos-uso/asociarMetodologiaDocenteAAsignaturaPrograma/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > asociarMetodologiaDocenteAAsignaturaPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/asociarMetodologiaDocenteAAsignaturaPrograma/README.md)|[Diseño](/RUP/03-diseño/casos-uso/asociarMetodologiaDocenteAAsignaturaPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAAsignaturaPrograma/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAAsignaturaPrograma/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorPrograma`, `Admin` (issue [#599](https://github.com/mmasias/pyCelda/issues/599))|
|**Objetivo**|Asociar una `MetodologiaDocente` (ya asociada a la `Materia`) a una `AsignaturaPrograma` concreta|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Primer caso de uso construido de la cascada `MetodologiaDocente` en dos pasos (`AsignaturaPrograma o-r- MetodologiaDocente`, hallazgo de la sesión de L4, ver [modelo del dominio](/RUP/00-modelo-del-dominio/README.md)) -- mismo patrón exacto que la cascada, ya cerrada, de `ResultadoAprendizaje`: el director reparte primero un subconjunto del catálogo institucional a cada `Materia` (`asociarMetodologiaDocenteAMateria()`), y después, de ese subconjunto ya asociado a la `Materia`, reparte a cada `AsignaturaPrograma` concreta dentro de ella. El selector solo ofrece las `MetodologiaDocente` que cumplen las dos condiciones -- ya asociadas a la `Materia` y no asociadas aún a esta `AsignaturaPrograma` -- por la regla de consistencia del modelo de dominio: las MD de una `AsignaturaPrograma` deben ser subconjunto de las ya asociadas a su `Materia`.

**Sin `editarAsociacionX()` propio**: a diferencia de `MetodologiaMateria` (que sí tiene atributo propio, `descripcionPropia`), la asociación `AsignaturaPrograma`-`MetodologiaDocente` es agregación simple sin atributo -- no hay nada que editar aparte de la propia pertenencia. Cierre de catálogo (completa el trío pendiente desde L4) y de forma en la discussion [#33](https://github.com/mmasias/pyCelda/discussions/33). Sin `<<choice>>`: asignación libre, mismo patrón que `asociarResultadoAprendizajeAAsignaturaPrograma()`.

**Actor `Admin` (issue [#599](https://github.com/mmasias/pyCelda/issues/599))**: `Admin` gana esta transición como vía de corrección excepcional, con paridad completa respecto a `DirectorPrograma` -- no sustituye su flujo normal, lo complementa. Misma ficha, mismo wireframe y mismas reglas; es un self-loop de `ASIGNATURA_PROGRAMA_ABIERTO` también en [diagramaContextoAdmin.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml). Sin alcance por programa: `Admin` actúa sobre cualquier `AsignaturaPrograma`.

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `ASIGNATURA_PROGRAMA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO : asociarMetodologiaDocenteAAsignaturaPrograma()`
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) -- catálogo de casos de uso de `DirectorPrograma` sobre `AsignaturaPrograma`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaPrograma o-r- MetodologiaDocente`; README, cascada en dos pasos y regla de consistencia (subconjunto de la `Materia`)
- [Discussion #33](https://github.com/mmasias/pyCelda/discussions/33) -- cierre del catálogo (completa el trío pendiente desde L4, resuelto como par) y de la forma de este caso de uso
- [`asociarMetodologiaDocenteAMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAMateria/README.md) -- primer escalón de la misma cascada
- [`desasociarMetodologiaDocenteAsignaturaPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteAsignaturaPrograma/README.md) -- caso de uso complementario (baja de la asociación)
