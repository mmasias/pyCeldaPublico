<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > asociarMetodologiaDocenteAAsignaturaGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAAsignaturaGrado/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAAsignaturaGrado/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorGrado`|
|**Objetivo**|Asociar una `MetodologiaDocente` (ya asociada a la `Materia`) a una `AsignaturaGrado` concreta|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Primer caso de uso construido de la cascada `MetodologiaDocente` en dos pasos (`AsignaturaGrado o-r- MetodologiaDocente`, hallazgo de la sesión de L4, ver modelo del dominio) -- mismo patrón exacto que la cascada, ya cerrada, de `ResultadoAprendizaje`: el director reparte primero un subconjunto del catálogo institucional a cada `Materia` (`asociarMetodologiaDocenteAMateria()`), y después, de ese subconjunto ya asociado a la `Materia`, reparte a cada `AsignaturaGrado` concreta dentro de ella. El selector solo ofrece las `MetodologiaDocente` que cumplen las dos condiciones -- ya asociadas a la `Materia` y no asociadas aún a esta `AsignaturaGrado` -- por la regla de consistencia del modelo de dominio: las MD de una `AsignaturaGrado` deben ser subconjunto de las ya asociadas a su `Materia`.

**Sin `editarAsociacionX()` propio**: a diferencia de `MetodologiaMateria` (que sí tiene atributo propio, `descripcionPropia`), la asociación `AsignaturaGrado`-`MetodologiaDocente` es agregación simple sin atributo -- no hay nada que editar aparte de la propia pertenencia. Cierre de catálogo (completa el trío pendiente desde L4) y de forma en la discussion [#33](https://github.com/mmasias/pyCelda/discussions/33). Sin `<<choice>>`: asignación libre, mismo patrón que `asociarResultadoAprendizajeAAsignaturaGrado()`.

## Referencias

- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `ASIGNATURA_GRADO_ABIERTO --> ASIGNATURA_GRADO_ABIERTO : asociarMetodologiaDocenteAAsignaturaGrado()`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- catálogo de casos de uso de `DirectorGrado` sobre `AsignaturaGrado`
- Modelo del dominio -- `AsignaturaGrado o-r- MetodologiaDocente`; README, cascada en dos pasos y regla de consistencia (subconjunto de la `Materia`)
- [Discussion #33](https://github.com/mmasias/pyCelda/discussions/33) -- cierre del catálogo (completa el trío pendiente desde L4, resuelto como par) y de la forma de este caso de uso
- [`asociarMetodologiaDocenteAMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAMateria/README.md) -- primer escalón de la misma cascada
- [`desasociarMetodologiaDocenteAsignaturaGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteAsignaturaGrado/README.md) -- caso de uso complementario (baja de la asociación)
