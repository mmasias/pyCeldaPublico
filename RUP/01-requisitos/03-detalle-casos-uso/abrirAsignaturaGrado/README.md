<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirAsignaturaGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturaGrado/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturaGrado/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Consultar los datos de una `AsignaturaGrado` concreta|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

Caso de uso reutilizado por `DirectorGrado`, misma ficha -- ver [diagramaContextoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml).

**Dos entradas, un solo retorno** -- mismo patrón que documenta el propio [diagramaContextoAdmin.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml): un atajo plano desde `GRADO_ABIERTO` (tabla de `AsignaturaGrado` agrupada por `Materia`, añadida en el retoque de [`abrirGrado()`](../abrirGrado/README.md)) y una segunda entrada desde la propia `MATERIA_ABIERTO` (retoque de [`abrirMateria()`](../abrirMateria/README.md)), pero un único retorno -- vuelve siempre a `GRADO_ABIERTO` reutilizando `abrirGrado()`, la entrada más lógica y previsiblemente más usada, no su padre por composición (`Materia`).

`ects` y `contenido` se muestran con su valor efectivo (heredado de `Asignatura` si no hay override propio, ver modelo del dominio); igual `nombre` cuando coincide con el de la `Asignatura` -- este caso de uso no distingue en pantalla si el valor es propio o heredado, esa distinción es de [`editarAsignaturaGrado()`](../editarAsignaturaGrado/README.md).

**Retocado el wireframe al construir L6** (mismo criterio que `abrirMateria()` en L4/L5 y `abrirGrado()` en L5, sin tocar la especificación): `ASIGNATURA_GRADO_ABIERTO` es el destino de los seis self-loops nuevos de asociación (`asignarProfesorAAsignaturaGrado()`/`desasignarProfesorAsignaturaGrado()`, `asociarResultadoAprendizajeAAsignaturaGrado()`/`desasociarResultadoAprendizajeAsignaturaGrado()`, `asociarMetodologiaDocenteAAsignaturaGrado()`/`desasociarMetodologiaDocenteAsignaturaGrado()`), así que el detalle necesita mostrar las tres listas para que esos botones tengan sentido. Ninguna de las tres lleva `[Editar]` por fila -- decisión cerrada en la discussion [#33](https://github.com/mmasias/pyCelda/discussions/33): ninguna de las tres relaciones tiene atributo propio, solo `[Quitar]`.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `GRADO_ABIERTO --> ASIGNATURA_GRADO_ABIERTO : abrirAsignaturaGrado()`, `MATERIA_ABIERTO --> ASIGNATURA_GRADO_ABIERTO : abrirAsignaturaGrado()`
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- mismas dos transiciones
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catálogo de casos de uso de `Admin` sobre `AsignaturaGrado`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- reutilización del caso de uso por `DirectorGrado`
- Modelo del dominio -- `AsignaturaGrado{nombre, curso, caracter, idioma, ects, semestreDefault, contenido, estado}`, herencia de `nombre`/`ects`/`contenido` sobre `Asignatura`
- [Discussion #33](https://github.com/mmasias/pyCelda/discussions/33) -- cierre del recuento y forma de L6, origen del retoque de este wireframe
