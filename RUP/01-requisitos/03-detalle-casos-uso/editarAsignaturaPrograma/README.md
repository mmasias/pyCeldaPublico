<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/editarAsignaturaPrograma/README.md) / [Diseño](/RUP/03-diseño/casos-uso/editarAsignaturaPrograma/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarAsignaturaPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/editarAsignaturaPrograma/README.md)|[Diseño](/RUP/03-diseño/casos-uso/editarAsignaturaPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarAsignaturaPrograma/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarAsignaturaPrograma/wireframe-completo.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarAsignaturaPrograma/wireframe-semestre-bloqueado.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorPrograma`, `Admin`|
|**Objetivo**|Modificar los datos de una `AsignaturaPrograma` de su `Programa`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

**Único caso de edición del catálogo, compartido por `DirectorPrograma` y `Admin`** (ficha única, caso de uso reutilizado por `Admin`, mismo patrón que [`abrirAsignaturaPrograma()`](../abrirAsignaturaPrograma/README.md); ver [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) y [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml)). Edita los 8 atributos propios de una vez, sin distinguir en el formulario entre los de identidad (`curso`, `carácter`, `idioma`, `semestre por defecto`) y los de override (`nombre`, `ects`, `contenido`, `requisitos previos`) -- esa distinción sí importa en [`crearAsignaturaPrograma()`](../crearAsignaturaPrograma/README.md) (dónde hay valor heredado que mostrar de partida), no aquí, donde todos los campos ya tienen un valor propio que mostrar. Único matiz: `semestre por defecto` deja de estar siempre disponible -- ver `<<choice>>` a continuación.

**`requisitos previos` (discussion [#259](https://github.com/mmasias/pyCelda/discussions/259), ítem 2 del backlog de [#217](https://github.com/mmasias/pyCelda/discussions/217))**: atributo de texto plano nuevo de `AsignaturaPrograma`, editable aquí junto a `contenido` (misma familia de campo de override redactado). Sustituye el literal `_REQUISITOS_PREVIOS_AQUI_` que la guía docente rendía crudo; el render lo lee **en vivo**, así que editarlo cambia el texto de las guías ya `Aprobada` que lo referencian -- deuda de congelado retroactivo compartida con los RA, se resuelve en el issue [#219](https://github.com/mmasias/pyCelda/issues/219), no aquí. `Admin` edita este mismo campo (ver nota de paridad a continuación).

**Paridad `Admin` con `DirectorPrograma` (issue [#602](https://github.com/mmasias/pyCelda/issues/602))**: `Admin` gana esta transición como vía de corrección excepcional, con paridad completa con `DirectorPrograma` -- los 8 atributos de arriba, incluido `contenido` (el override que gobierna a Director y Profesor), sin alcance por programa (`Admin` no tiene programa propio). Además de esos 8, `Admin` conserva los dos atributos que solo él edita (`materia`, `sesiones mínimas`), que no pertenecen a este caso de uso compartido, y el `<<choice>>` de `semestreDefault` aplica igual para ambos actores. Mismo patrón de corrección que [#599](https://github.com/mmasias/pyCelda/issues/599). Cierra también un hueco anterior: el `editarAsignaturaProgramaAdmin()` que ya existía (`materia`, `curso`, `carácter`, `sesiones mínimas`) nunca tuvo su self-loop en el diagrama de contexto de `Admin`.

**Resuelto (2026-08-19): `<<choice>>` de bloqueo sobre `semestreDefault`**. El [modelo del dominio](/RUP/00-modelo-del-dominio/README.md) señala `semestreDefault` como invariante una vez que alguna `Guia` se ha creado apoyándose en él -- no antes. Con el hilo `Guia` (L7-L9) ya cerrado hasta Desarrollo, la condición es comprobable, así que el `<<choice>>` señalado como pendiente desde antes de L7-L9 se formaliza ahora. **No es el mismo patrón que `editarCursoAcademico()`**: allí el `<<choice>>` bloquea el caso de uso entero (solo edita 2 campos, ambos parte de la misma invariante); aquí edita 8 campos y solo uno es condicionalmente invariante, así que el `<<choice>>` bifurca la presentación del formulario, no el caso de uso -- una rama presenta los 8 campos editables, la otra presenta los 7 no condicionados más `semestreDefault` bloqueado con su motivo visible. Ambas ramas son camino feliz (verde): no hay fallo de precondición del sistema, solo una variante de qué campos admite el formulario.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `ASIGNATURA_PROGRAMA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO : editarAsignaturaPrograma()`
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `ASIGNATURA_PROGRAMA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO : editarAsignaturaPrograma()`
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) -- catálogo de casos de uso de `DirectorPrograma` sobre `AsignaturaPrograma`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaPrograma{nombre, curso, caracter, idioma, ects, semestreDefault, contenido, requisitosPrevios, estado}`; README, herencia de `nombre`/`ects`/`contenido`, invarianza condicional de `semestreDefault`, `requisitosPrevios` como texto plano en vivo (discussion [#259](https://github.com/mmasias/pyCelda/discussions/259))
