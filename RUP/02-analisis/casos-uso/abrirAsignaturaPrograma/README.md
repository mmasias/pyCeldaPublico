<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirAsignaturaPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturaPrograma/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirAsignaturaPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirAsignaturaPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturaPrograma/README.md): un solo paso, sin `<<choice>>`, de solo lectura, con dos entradas -- mismo patrón que documenta la propia especificación de Requisitos. Ambos actores vuelven por dos caminos, uno por entrada (`abrirPrograma()` y `abrirMateria()`, ver Requisitos); esta ficha modela `DirectorPrograma`, con esos dos retornos. Presenta los datos propios de la `AsignaturaPrograma` y sus tres colecciones asociadas: profesorado, `MetodologiaDocente` y `ResultadoAprendizaje`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirAsignaturaPrograma/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirAsignaturaProgramaView`

**Responsabilidades:**
- presenta `nombre`, `curso`, `caracter`, `idioma`, `ects`, `semestreDefault`, `contenido`, `requisitosPrevios`, `estado` de la `AsignaturaPrograma`.
- presenta el profesorado asignado, con navegación a quitar cada uno (gestión fuera de alcance, ver más abajo).
- presenta los `ResultadoAprendizaje` asociados, con navegación a quitar cada uno.
- presenta las `MetodologiaDocente` asociadas, con navegación a quitar cada una.
- ofrece la navegación a asociar nuevo profesorado/RA/MD, editar la `AsignaturaPrograma` y volver al `Programa`.

**Colaboraciones:**
- **Entrada:** `:PROGRAMA_ABIERTO` (atajo plano) o `:MATERIA_ABIERTO` (segunda entrada) -- el `DirectorPrograma` solicita abrir una `AsignaturaPrograma`.
- **Control:** `AsignaturaProgramaController`.
- **Salida:** `:PROGRAMA_ABIERTO` vía [`abrirPrograma()`](../abrirPrograma/README.md) o `:MATERIA_ABIERTO` vía [`abrirMateria()`](../abrirMateria/README.md) -- un retorno por entrada, resultado de dos oleadas del patrón de reversión sobre uso real de discussion [#227](https://github.com/mmasias/pyCelda/discussions/227) (`DirectorPrograma` 2026-09-04, `Admin` issue [#252](https://github.com/mmasias/pyCelda/issues/252)). Decisión de navegación del cliente: ambos reutilizan el `GET` ya resuelto por `AbrirAsignaturaProgramaView`, sin colaboración nueva.

## Clases de controlador

### `AsignaturaProgramaController`

**Responsabilidades:**
- recupera la `AsignaturaPrograma` (`cargarAsignaturaPrograma(asignaturaProgramaId)`) para sus datos propios.
- lista las `MetodologiaDocente`/`ResultadoAprendizaje` asociadas y el profesorado asignado.
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirAsignaturaProgramaView`.
- **Salida:** `AsignaturaProgramaRepository`.

## Clases de modelo

### `AsignaturaPrograma`

**Responsabilidades:**
- porta sus nueve atributos propios (`requisitosPrevios` incluido, discussion [#259](https://github.com/mmasias/pyCelda/discussions/259)) y compone sus tres colecciones asociadas (profesorado, `MetodologiaDocente`, `ResultadoAprendizaje`).

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`, vía `AsignaturaProgramaRepository`.
- **Salida:** compone `MetodologiaDocente`, `ResultadoAprendizaje`, `Profesor`.

### `AsignaturaProgramaRepository`

**Responsabilidades:**
- recupera la `AsignaturaPrograma` por identificador (`obtener(asignaturaProgramaId)`).
- lista las `MetodologiaDocente`/`ResultadoAprendizaje` asociadas y el profesorado asignado.

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`.
- **Salida:** gestiona `AsignaturaPrograma`.

### `MetodologiaDocente`

**Responsabilidades:**
- porta `codigo`, `descripcion` -- mostrados en la lista de asociadas.

**Colaboraciones:**
- **Entrada:** listada por `AsignaturaProgramaRepository`.

### `ResultadoAprendizaje`

**Responsabilidades:**
- porta `codigo`, `tipo` -- mostrados en la lista de asociados.

**Colaboraciones:**
- **Entrada:** listado por `AsignaturaProgramaRepository`.

### `Profesor`

**Responsabilidades:**
- porta `nombre` -- mostrado en la lista de profesorado asignado, de solo lectura.

**Colaboraciones:**
- **Entrada:** listado por `AsignaturaProgramaRepository`.

## Simplificación fuera de alcance de esta rebanada

**Gestión de profesorado**: `asignarProfesorAAsignaturaPrograma()`/`desasignarProfesorAsignaturaPrograma()` son exclusivos de `Admin` (ver [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml)), fuera de alcance de esta rebanada de `DirectorPrograma` (discussion [#65](https://github.com/mmasias/pyCelda/discussions/65)). Este diagrama modela solo la lectura del profesorado ya asignado -- dato ya presente en el modelo de dominio (`AsignaturaPrograma -- Profesor`), sin botón de gestión propio.

**Ninguna de las tres listas lleva `[Editar]` por fila**: decisión ya cerrada en Requisitos (discussion [#33](https://github.com/mmasias/pyCelda/discussions/33)) -- ninguna de las tres relaciones tiene atributo propio que editar, solo `[Quitar]`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturaPrograma/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturaPrograma/wireframes.puml) -- fuente de verdad del contenido presentado.
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `PROGRAMA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO : abrirAsignaturaPrograma()`, `MATERIA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO : abrirAsignaturaPrograma()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaPrograma{nombre, curso, caracter, idioma, ects, semestreDefault, contenido, requisitosPrevios, estado}`, `AsignaturaPrograma -- Profesor`, `AsignaturaPrograma o-r- MetodologiaDocente`, `AsignaturaPrograma o- ResultadoAprendizaje`.
- [`editarAsignaturaPrograma()`](../editarAsignaturaPrograma/README.md) -- edición de los datos propios que este caso de uso presenta de solo lectura.
- [`editarActividadesFormativasAsignaturaPrograma()`](../editarActividadesFormativasAsignaturaPrograma/README.md) -- el clúster de `ActividadFormativa` (discussion [#227](https://github.com/mmasias/pyCelda/discussions/227)) añade una cuarta colección (las 10 `ActividadFormativaAsignaturaPrograma`, con `horas` y `porcentajePresencialidad`); la fusión en `abrirAsignaturaPrograma()` y el cambio de `AsignaturaProgramaDetalleResponse` se detallan al construir el clúster (audit del agregado `AsignaturaPrograma`).
