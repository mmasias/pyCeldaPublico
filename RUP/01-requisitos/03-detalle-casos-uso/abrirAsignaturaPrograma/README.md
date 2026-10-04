<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/abrirAsignaturaPrograma/README.md) / [Diseño](/RUP/03-diseño/casos-uso/abrirAsignaturaPrograma/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirAsignaturaPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/abrirAsignaturaPrograma/README.md)|[Diseño](/RUP/03-diseño/casos-uso/abrirAsignaturaPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturaPrograma/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturaPrograma/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`, `DirectorPrograma`|
|**Objetivo**|Consultar los datos de una `AsignaturaPrograma` concreta|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

Caso de uso reutilizado por `DirectorPrograma`, misma ficha -- ver [diagramaContextoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml).

**Dos entradas** en ambos actores -- un atajo plano desde `PROGRAMA_ABIERTO` (tabla de `AsignaturaPrograma` agrupada por `Materia`, añadida en el retoque de [`abrirPrograma()`](../abrirPrograma/README.md)) y una segunda entrada desde la propia `MATERIA_ABIERTO` (retoque de [`abrirMateria()`](../abrirMateria/README.md)).

**Ambos actores vuelven por dos caminos** ("Volver al Programa" y "Volver a la materia"), reutilizando `abrirPrograma()` y `abrirMateria()` -- uno por cada entrada, no el padre por composición (`Materia *-- AsignaturaPrograma`) tratado como retorno único. El retorno único original ("vuelve siempre a `PROGRAMA_ABIERTO`, la entrada más lógica y previsiblemente más usada") se revirtió en dos oleadas del mismo patrón de reversión sobre uso real ya usado en discussion [#227](https://github.com/mmasias/pyCelda/discussions/227)/PR [#234](https://github.com/mmasias/pyCelda/pull/234) ("el Profesor no ve las actividades formativas"): `DirectorPrograma` ganó el segundo retorno primero (retoque de Manuel usando el producto, 2026-09-04, relay vía pySigHor); `Admin` lo ganó después con el mismo argumento (issue [#252](https://github.com/mmasias/pyCelda/issues/252), 2026-09-05) -- volver siempre al `Programa` resultaba igual de incómodo para quien había entrado desde `MATERIA_ABIERTO`. Incondicional en los dos, sin guarda de rol nueva -- el mismo actor ya tiene acceso a `MATERIA_ABIERTO` por la entrada de arriba; `materia_id` viaja en la respuesta, sin dato ni endpoint nuevo. `Admin` y `DirectorPrograma` son componentes de frontend distintos (`AsignaturaProgramaAdmin.tsx` / `AsignaturaPrograma.tsx`) que aterrizan en pantallas de `Materia` distintas (`MateriaAdmin.tsx` / `Materia.tsx`) pese a compartir esta ficha de Requisitos, pero como ahora los dos llevan los mismos dos botones de retorno el único wireframe compartido ya no necesita anotación por actor.

`ects` y `contenido` se muestran con su valor efectivo (heredado de `Asignatura` si no hay override propio, ver [modelo del dominio](/RUP/00-modelo-del-dominio/README.md)); igual `nombre` cuando coincide con el de la `Asignatura` -- este caso de uso no distingue en pantalla si el valor es propio o heredado, esa distinción es de [`editarAsignaturaPrograma()`](../editarAsignaturaPrograma/README.md). `requisitosPrevios` (texto plano, discussion [#259](https://github.com/mmasias/pyCelda/discussions/259)) se muestra tal cual, sin herencia -- es propio de `AsignaturaPrograma`, no de `Asignatura`.

**Retocado el wireframe al construir L6** (mismo criterio que `abrirMateria()` en L4/L5 y `abrirPrograma()` en L5, sin tocar la especificación): `ASIGNATURA_PROGRAMA_ABIERTO` es el destino de los seis self-loops nuevos de asociación (`asignarProfesorAAsignaturaPrograma()`/`desasignarProfesorAsignaturaPrograma()`, `asociarResultadoAprendizajeAAsignaturaPrograma()`/`desasociarResultadoAprendizajeAsignaturaPrograma()`, `asociarMetodologiaDocenteAAsignaturaPrograma()`/`desasociarMetodologiaDocenteAsignaturaPrograma()`), así que el detalle necesita mostrar las tres listas para que esos botones tengan sentido. Ninguna de las tres lleva `[Editar]` por fila -- decisión cerrada en la discussion [#33](https://github.com/mmasias/pyCelda/discussions/33): ninguna de las tres relaciones tiene atributo propio, solo `[Quitar]`.

**Retocado de nuevo al construir el clúster de `ActividadFormativa` (discussion [#227](https://github.com/mmasias/pyCelda/discussions/227))**: `ASIGNATURA_PROGRAMA_ABIERTO` gana la sección "Actividades formativas" -- las 10 actividades formativas siempre presentes con sus `horas` y `porcentajePresencialidad`, y un botón `[Editar reparto]` -> [`editarActividadesFormativasAsignaturaPrograma()`](../editarActividadesFormativasAsignaturaPrograma/README.md) (self-loop). A diferencia de las tres listas anteriores, aquí sí hay valores por fila que editar (`horas`, `%`), pero igual que ellas **no** hay `+ Asociar`/`[Quitar]`: las 10 filas se autopueblan a 0 al crear la `AsignaturaPrograma`. Este nivel es el que consume el render de la `Guia` (sección 4 del formulario oficial). No se toca la especificación de `abrirAsignaturaPrograma()`.

**Paridad `Admin` con `DirectorPrograma` (issue [#599](https://github.com/mmasias/pyCelda/issues/599))**: `AsignaturaProgramaAdmin.tsx` muestra también las secciones de Resultados de aprendizaje, Metodologías docentes y Actividades formativas -- el wireframe compartido ya las contenía, sin cambios. `ASIGNATURA_PROGRAMA_ABIERTO` de `Admin` gana cinco self-loops (`asociarResultadoAprendizajeAAsignaturaPrograma()`, `desasociarResultadoAprendizajeAsignaturaPrograma()`, `asociarMetodologiaDocenteAAsignaturaPrograma()`, `desasociarMetodologiaDocenteAsignaturaPrograma()`, `editarActividadesFormativasAsignaturaPrograma()`).

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROGRAMA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO : abrirAsignaturaPrograma()`, `MATERIA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO : abrirAsignaturaPrograma()`, dos retornos `ASIGNATURA_PROGRAMA_ABIERTO --> PROGRAMA_ABIERTO : abrirPrograma()` y `ASIGNATURA_PROGRAMA_ABIERTO --> MATERIA_ABIERTO : abrirMateria()` (issue [#252](https://github.com/mmasias/pyCelda/issues/252))
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- mismas dos entradas y los mismos dos retornos: `abrirPrograma()` y `abrirMateria()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catálogo de casos de uso de `Admin` sobre `AsignaturaPrograma`
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) -- reutilización del caso de uso por `DirectorPrograma`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaPrograma{nombre, curso, caracter, idioma, ects, semestreDefault, contenido, requisitosPrevios, estado}`, herencia de `nombre`/`ects`/`contenido` sobre `Asignatura`
- [Discussion #33](https://github.com/mmasias/pyCelda/discussions/33) -- cierre del recuento y forma de L6, origen del retoque de este wireframe
- [Discussion #227](https://github.com/mmasias/pyCelda/discussions/227) / [PR #234](https://github.com/mmasias/pyCelda/pull/234) -- precedente del patrón de reversión sobre uso real aplicado aquí a los dos segundos retornos (`DirectorPrograma` 2026-09-04, `Admin` issue [#252](https://github.com/mmasias/pyCelda/issues/252))
- [Issue #253](https://github.com/mmasias/pyCelda/issues/253) -- purga de "módulo" como sinónimo de `Materia`: el botón de retorno pasa de "Volver al módulo" a "Volver a la materia"
