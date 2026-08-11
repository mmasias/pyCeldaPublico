<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > editarSemestreGuia()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarSemestreGuia/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarSemestreGuia/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorGrado`|
|**Objetivo**|Ajustar el `semestre` de una `Guia` concreta cuando difiere de `semestreDefault` de su `AsignaturaGrado`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Formaliza el override ya cerrado en el modelo de dominio: `semestreDefault` (`AsignaturaGrado`) es invariante -- cambiarlo implica un `Grado` nuevo -- pero `semestre` en `Guia` es el ajuste puntual que hace el `DirectorGrado`, no el `Profesor`, para casos reales como grupos especiales o asignaturas que se imparten en los dos semestres del mismo curso (el caso real que lo confirmó es exactamente `GII__IYA003`, Programación I).

**`editarX()` simple, self-loop de `GUIA_ABIERTO`**: sin transición de estado propia en `guia.puml` -- si la `Guia` estaba `Aprobada`, el único efecto colateral es que se regenera el PDF y se actualiza `fechaGeneracionPDF`, narrado en prosa en la nota de la transición de salida, mismo mecanismo que usa [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) para narrar "estado pasa a Borrador" sin abrir una rama nueva. Si además el `DirectorGrado` quiere que el `Profesor` revise el cambio, compone este caso de uso con [`revocarAprobacionGuia()`](../revocarAprobacionGuia/README.md) en vez de que `editarSemestreGuia()` ramifique la máquina de estados -- decisión ya cerrada en el modelo de dominio, sin discussion de L9.

Wireframe con dato real, sin hipótesis: `GII__IYA003` en semestre 1, editado a semestre 2 -- el caso real que motivó este caso de uso (Programación I se imparte en los dos semestres del curso).

## Referencias

- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `GUIA_ABIERTO --> GUIA_ABIERTO : editarSemestreGuia()`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- catálogo de casos de uso de `DirectorGrado` sobre `Guia`
- Modelo del dominio -- entrada "`semestreDefault` (en `AsignaturaGrado`) es invariante", patrón catálogo+override
- Modelo del dominio -- `Guia{semestre}`, `AsignaturaGrado{semestreDefault}`
- [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) -- mismo mecanismo de narrar en prosa un efecto colateral sobre el estado sin rama nueva
