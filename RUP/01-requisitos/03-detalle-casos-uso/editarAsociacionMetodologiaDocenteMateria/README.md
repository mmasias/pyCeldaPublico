<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > editarAsociacionMetodologiaDocenteMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarAsociacionMetodologiaDocenteMateria/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarAsociacionMetodologiaDocenteMateria/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorGrado`|
|**Objetivo**|Editar `descripcionPropia` de la asociación entre una `Materia` y una `MetodologiaDocente`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Único campo editable: `descripcionPropia` de `MetodologiaMateria`. `codigo` y `descripcion` de la `MetodologiaDocente` se muestran de solo lectura (pertenecen al catálogo institucional, se editan desde [`editarMetodologiaDocente()`](/RUP/01-requisitos/03-detalle-casos-uso/editarMetodologiaDocente/README.md), no desde aquí). Patrón catálogo+override, mismo que `nombre`/`ects` en `AsignaturaGrado` o `semestre` en `Guia`: vacío por defecto (usa la descripción canónica), y este caso de uso es donde el director registra el matiz si lo necesita.

## Referencias

- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `MATERIA_ABIERTO --> MATERIA_ABIERTO : editarAsociacionMetodologiaDocenteMateria()`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- catálogo de casos de uso de `DirectorGrado` sobre `Materia`
- Modelo del dominio -- `MetodologiaMateria{descripcionPropia}`, README: "vacío por defecto... si el director de una materia concreta necesita un matiz distinto, lo registra en `descripcionPropia`"
- [Discussion #27](https://github.com/mmasias/pyCelda/discussions/27) -- cierre del hueco de verbos de asociación a nivel de `Materia`
