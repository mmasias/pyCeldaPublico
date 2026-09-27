<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > abrirAsignaturaGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturaGrado/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirAsignaturaGrado/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirAsignaturaGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturaGrado/README.md): un solo paso, sin `<<choice>>`, de solo lectura, con dos entradas -- mismo patrón que documenta la propia especificación de Requisitos. Ambos actores vuelven por dos caminos, uno por entrada (`abrirGrado()` y `abrirMateria()`, ver Requisitos); esta ficha modela `DirectorGrado`, con esos dos retornos. Presenta los datos propios de la `AsignaturaGrado` y sus tres colecciones asociadas: profesorado, `MetodologiaDocente` y `ResultadoAprendizaje`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirAsignaturaGrado/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirAsignaturaGradoView`

**Responsabilidades:**
- presenta `nombre`, `curso`, `caracter`, `idioma`, `ects`, `semestreDefault`, `contenido`, `requisitosPrevios`, `estado` de la `AsignaturaGrado`.
- presenta el profesorado asignado, con navegación a quitar cada uno (gestión fuera de alcance, ver más abajo).
- presenta los `ResultadoAprendizaje` asociados, con navegación a quitar cada uno.
- presenta las `MetodologiaDocente` asociadas, con navegación a quitar cada una.
- ofrece la navegación a asociar nuevo profesorado/RA/MD, editar la `AsignaturaGrado` y volver al `Grado`.

**Colaboraciones:**
- **Entrada:** `:GRADO_ABIERTO` (atajo plano) o `:MATERIA_ABIERTO` (segunda entrada) -- el `DirectorGrado` solicita abrir una `AsignaturaGrado`.
- **Control:** `AsignaturaGradoController`.
- **Salida:** `:GRADO_ABIERTO` vía [`abrirGrado()`](../abrirGrado/README.md) o `:MATERIA_ABIERTO` vía [`abrirMateria()`](../abrirMateria/README.md) -- un retorno por entrada, resultado de dos oleadas del patrón de reversión sobre uso real de discussion [#227](https://github.com/mmasias/pyCelda/discussions/227) (`DirectorGrado` 2026-09-04, `Admin` issue [#252](https://github.com/mmasias/pyCelda/issues/252)). Decisión de navegación del cliente: ambos reutilizan el `GET` ya resuelto por `AbrirAsignaturaGradoView`, sin colaboración nueva.

## Clases de controlador

### `AsignaturaGradoController`

**Responsabilidades:**
- recupera la `AsignaturaGrado` (`cargarAsignaturaGrado(asignaturaGradoId)`) para sus datos propios.
- lista las `MetodologiaDocente`/`ResultadoAprendizaje` asociadas y el profesorado asignado.
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirAsignaturaGradoView`.
- **Salida:** `AsignaturaGradoRepository`.

## Clases de modelo

### `AsignaturaGrado`

**Responsabilidades:**
- porta sus nueve atributos propios (`requisitosPrevios` incluido, discussion [#259](https://github.com/mmasias/pyCelda/discussions/259)) y compone sus tres colecciones asociadas (profesorado, `MetodologiaDocente`, `ResultadoAprendizaje`).

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`, vía `AsignaturaGradoRepository`.
- **Salida:** compone `MetodologiaDocente`, `ResultadoAprendizaje`, `Profesor`.

### `AsignaturaGradoRepository`

**Responsabilidades:**
- recupera la `AsignaturaGrado` por identificador (`obtener(asignaturaGradoId)`).
- lista las `MetodologiaDocente`/`ResultadoAprendizaje` asociadas y el profesorado asignado.

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`.
- **Salida:** gestiona `AsignaturaGrado`.

### `MetodologiaDocente`

**Responsabilidades:**
- porta `codigo`, `descripcion` -- mostrados en la lista de asociadas.

**Colaboraciones:**
- **Entrada:** listada por `AsignaturaGradoRepository`.

### `ResultadoAprendizaje`

**Responsabilidades:**
- porta `codigo`, `tipo` -- mostrados en la lista de asociados.

**Colaboraciones:**
- **Entrada:** listado por `AsignaturaGradoRepository`.

### `Profesor`

**Responsabilidades:**
- porta `nombre` -- mostrado en la lista de profesorado asignado, de solo lectura.

**Colaboraciones:**
- **Entrada:** listado por `AsignaturaGradoRepository`.

## Simplificación fuera de alcance de esta rebanada

**Gestión de profesorado**: `asignarProfesorAAsignaturaGrado()`/`desasignarProfesorAsignaturaGrado()` son exclusivos de `Admin` (ver [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml)), fuera de alcance de esta rebanada de `DirectorGrado` (discussion [#65](https://github.com/mmasias/pyCelda/discussions/65)). Este diagrama modela solo la lectura del profesorado ya asignado -- dato ya presente en el modelo de dominio (`AsignaturaGrado -- Profesor`), sin botón de gestión propio.

**Ninguna de las tres listas lleva `[Editar]` por fila**: decisión ya cerrada en Requisitos (discussion [#33](https://github.com/mmasias/pyCelda/discussions/33)) -- ninguna de las tres relaciones tiene atributo propio que editar, solo `[Quitar]`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturaGrado/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturaGrado/wireframes.puml) -- fuente de verdad del contenido presentado.
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `GRADO_ABIERTO --> ASIGNATURA_GRADO_ABIERTO : abrirAsignaturaGrado()`, `MATERIA_ABIERTO --> ASIGNATURA_GRADO_ABIERTO : abrirAsignaturaGrado()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaGrado{nombre, curso, caracter, idioma, ects, semestreDefault, contenido, requisitosPrevios, estado}`, `AsignaturaGrado -- Profesor`, `AsignaturaGrado o-r- MetodologiaDocente`, `AsignaturaGrado o- ResultadoAprendizaje`.
- [`editarAsignaturaGrado()`](../editarAsignaturaGrado/README.md) -- edición de los datos propios que este caso de uso presenta de solo lectura.
- [`editarActividadesFormativasAsignaturaGrado()`](../editarActividadesFormativasAsignaturaGrado/README.md) -- el clúster de `ActividadFormativa` (discussion [#227](https://github.com/mmasias/pyCelda/discussions/227)) añade una cuarta colección (las 10 `ActividadFormativaAsignaturaGrado`, con `horas` y `porcentajePresencialidad`); la fusión en `abrirAsignaturaGrado()` y el cambio de `AsignaturaGradoDetalleResponse` se detallan al construir el clúster (audit del agregado `AsignaturaGrado`).
