<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > editarAsignaturaGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarAsignaturaGrado/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarAsignaturaGrado/wireframe-completo.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarAsignaturaGrado/wireframe-semestre-bloqueado.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorGrado`|
|**Objetivo**|Modificar los datos de una `AsignaturaGrado` de su `Grado`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

**Único caso de edición del catálogo, y no es de `Admin`**: `Admin` crea, abre y elimina `AsignaturaGrado` (ver [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml)), pero no tiene `editarAsignaturaGrado()` propio -- es exclusivo de `DirectorGrado` (ver [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml)). Edita los 8 atributos propios de una vez, sin distinguir en el formulario entre los de identidad (`curso`, `carácter`, `idioma`, `semestre por defecto`) y los de override (`nombre`, `ects`, `contenido`, `requisitos previos`) -- esa distinción sí importa en [`crearAsignaturaGrado()`](../crearAsignaturaGrado/README.md) (dónde hay valor heredado que mostrar de partida), no aquí, donde todos los campos ya tienen un valor propio que mostrar. Único matiz: `semestre por defecto` deja de estar siempre disponible -- ver `<<choice>>` a continuación.

**`requisitos previos` (discussion [#259](https://github.com/mmasias/pyCelda/discussions/259), ítem 2 del backlog de [#217](https://github.com/mmasias/pyCelda/discussions/217))**: atributo de texto plano nuevo de `AsignaturaGrado`, editable aquí junto a `contenido` (misma familia de campo de override redactado). Sustituye el literal `_REQUISITOS_PREVIOS_AQUI_` que la guía docente rendía crudo; el render lo lee **en vivo**, así que editarlo cambia el texto de las guías ya `Aprobada` que lo referencian -- deuda de congelado retroactivo compartida con los RA, se resuelve en el issue [#219](https://github.com/mmasias/pyCelda/issues/219), no aquí. No se añade a `editarAsignaturaGradoAdmin()` (`Admin`), coherente con que `contenido` tampoco es Admin-editable.

**Resuelto (2026-08-19): `<<choice>>` de bloqueo sobre `semestreDefault`**. El [modelo del dominio](/RUP/00-modelo-del-dominio/README.md) señala `semestreDefault` como invariante una vez que alguna `Guia` se ha creado apoyándose en él -- no antes. Con el hilo `Guia` (L7-L9) ya cerrado hasta Desarrollo, la condición es comprobable, así que el `<<choice>>` señalado como pendiente desde antes de L7-L9 se formaliza ahora. **No es el mismo patrón que `editarCursoAcademico()`**: allí el `<<choice>>` bloquea el caso de uso entero (solo edita 2 campos, ambos parte de la misma invariante); aquí edita 8 campos y solo uno es condicionalmente invariante, así que el `<<choice>>` bifurca la presentación del formulario, no el caso de uso -- una rama presenta los 8 campos editables, la otra presenta los 7 no condicionados más `semestreDefault` bloqueado con su motivo visible. Ambas ramas son camino feliz (verde): no hay fallo de precondición del sistema, solo una variante de qué campos admite el formulario.

## Referencias

- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `ASIGNATURA_GRADO_ABIERTO --> ASIGNATURA_GRADO_ABIERTO : editarAsignaturaGrado()`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- catálogo de casos de uso de `DirectorGrado` sobre `AsignaturaGrado`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaGrado{nombre, curso, caracter, idioma, ects, semestreDefault, contenido, requisitosPrevios, estado}`; README, herencia de `nombre`/`ects`/`contenido`, invarianza condicional de `semestreDefault`, `requisitosPrevios` como texto plano en vivo (discussion [#259](https://github.com/mmasias/pyCelda/discussions/259))
