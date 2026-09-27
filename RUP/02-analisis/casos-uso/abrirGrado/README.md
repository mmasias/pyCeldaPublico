<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > abrirGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirGrado/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirGrado/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirGrado/README.md), en sus dos variantes: un solo paso, sin `<<choice>>`, de solo lectura en ambas. La `Admin` es "la misma ficha" con más acciones: además de la tabla de `AsignaturaGrado` (plana, con columna `Estado`, sin agrupar por `Materia`), ofrece el enlace "Ver Materias" (a [`abrirMaterias()`](../abrirMaterias/README.md)) y los botones `+ Crear AsignaturaGrado` ([`crearAsignaturaGrado()`](../crearAsignaturaGrado/README.md)) y `[Eliminar]` por fila ([`eliminarAsignaturaGrado()`](../eliminarAsignaturaGrado/README.md)) -- ambos exclusivos de `Admin`. Sin cambio en este retoque.

**`DirectorGrado` -- retocado (2026-09-05, Manuel usando el producto)**: presentaba los datos propios del `Grado` y sus `AsignaturaGrado` agrupadas por `Materia`; pasa a presentar el listado de `Guia` del `Grado` -- mismas clases de colaboración que [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) (`listarGuiasDelGrado(gradoId)`/`GuiaRepository.listarDelGrado(gradoId)`), reutilizadas tal cual desde esta segunda pantalla. Motivo: la tabla de `AsignaturaGrado` era un duplicado exacto de la propia pestaña [`abrirAsignaturasGrado()`](../abrirAsignaturasGrado/README.md) heredado del wireframe de `Admin`, sin enlace real a ninguna `Guia`. **Variante conservadora**: no se fusiona con `consultarEstadoGuias()` -- ambos casos de uso siguen siendo colaboraciones distintas, con sus propios diagramas, esta pantalla simplemente reutiliza el mismo par Controlador/Repositorio que aquel. Redundancia documental aceptada, no de código (mismo método real detrás de las dos pantallas).

Este `colaboracion.puml` contiene **dos diagramas**: el primero (`abrirGrado-analisis`) es la variante `DirectorGrado`; el segundo (`abrirGrado-admin-analisis`) es la variante `Admin` -- mismo criterio de troceo que `secuencia.puml` de `iniciarSesion()` y de la variante Admin de [`abrirGrados()`](../abrirGrados/README.md).

<div align=center>

|`DirectorGrado`|`Admin`|
|:-:|:-:|
|![](/images/RUP/02-analisis/casos-uso/abrirGrado/colaboracion.svg)|![](/images/RUP/02-analisis/casos-uso/abrirGrado/colaboracion-admin.svg)|
|<sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup>|<sup>mismo fichero, segundo bloque `@startuml`</sup>|

</div>

## Clases de vista

### `AbrirGradoView`

**Responsabilidades (variante DirectorGrado, retocada)**:
- presenta `codigo`, `nombre`, `estado` del `Grado`.
- presenta el listado de `Guia` del `Grado` (`AsignaturaGrado`, profesorado, estado, última actualización) -- antes la tabla de `AsignaturaGrado` agrupada por `Materia`, retirada de esta pantalla (sigue intacta en [`abrirAsignaturasGrado()`](../abrirAsignaturasGrado/README.md)).
- ofrece la navegación a abrir cada `Guia` ([`abrirGuia()`](../abrirGuia/README.md), reutilizado) y el botón `Notificar guías actualizadas` ([`notificarGuiasActualizadas()`](../notificarGuiasActualizadas/README.md), reutilizado) -- mismo contenido y mismas colaboraciones que [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md), duplicadas aquí a propósito.

**Responsabilidades (variante Admin):**
- presenta `codigo`, `nombre`, `estado` del `Grado`.
- presenta la tabla de `AsignaturaGrado` (asignatura, materia, curso, carácter, estado) del `Grado`, con `[Abrir]` por fila deshabilitado en esta rebanada y `[Eliminar]` activo (navega a la confirmación de [`eliminarAsignaturaGrado()`](../eliminarAsignaturaGrado/README.md)).
- ofrece el enlace "Ver Materias" (a [`abrirMaterias()`](../abrirMaterias/README.md)), el botón `+ Crear AsignaturaGrado` (a [`crearAsignaturaGrado()`](../crearAsignaturaGrado/README.md)), y la navegación a editar/eliminar el propio `Grado` y volver al listado de su `Facultad`.

**Colaboraciones:**
- **Entrada:** `:GRADOS_ABIERTO` -- el `DirectorGrado` o el `Admin` solicita abrir un `Grado`.
- **Control:** `GradoController`.
- **Salida:** `:GRADO_ABIERTO`.

## Clases de controlador

### `GradoController`

**Responsabilidades (variante DirectorGrado, retocada):**
- recupera el `Grado` (`cargarGrado(gradoId)`) para sus datos propios.
- lista las `Guia` del `Grado` (`listarGuiasDelGrado(gradoId)`) para el listado -- antes `listarAsignaturasGrado(gradoId)`; mismo método real que ya usaba `GuiaController` en [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md), reutilizado detrás de esta segunda Vista.

**Responsabilidades (variante Admin, sin cambio):**
- recupera el `Grado` (`cargarGrado(gradoId)`) para sus datos propios.
- lista las `AsignaturaGrado` del `Grado` (`listarAsignaturasGrado(gradoId)`) para la tabla.

No valida ni muta nada en ninguna de las dos -- caso de uso de solo lectura en ambas variantes.

**Colaboraciones:**
- **Entrada:** `AbrirGradoView`.
- **Salida (DirectorGrado):** `GradoRepository`, `GuiaRepository`.
- **Salida (Admin):** `GradoRepository`, `AsignaturaGradoRepository`.

## Clases de modelo

### `Grado`

**Responsabilidades:**
- porta `codigo` y `estado`.

**Colaboraciones:**
- **Entrada:** `GradoController`, vía `GradoRepository`.

### `GradoRepository`

**Responsabilidades:**
- recupera el `Grado` por identificador (`obtener(gradoId)`).

**Colaboraciones:**
- **Entrada:** `GradoController`.
- **Salida:** gestiona `Grado`.

### `Guia` (variante DirectorGrado, nueva en esta ficha)

**Responsabilidades:**
- porta `estado` y su `AsignaturaGrado`/profesorado asociados -- mismas responsabilidades que documenta [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md), aquí mostradas desde una segunda Vista.

**Colaboraciones:**
- **Entrada:** listada por `GuiaRepository`.

### `GuiaRepository` (variante DirectorGrado, nueva en esta ficha)

**Responsabilidades:**
- lista las `Guia` de un `Grado` (`listarDelGrado(gradoId)`) -- mismo método que ya existía para [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md), sin cambio de firma ni de comportamiento.

**Colaboraciones:**
- **Entrada:** `GradoController`.
- **Salida:** gestiona `Guia`.

### `AsignaturaGrado` (variante Admin, sin cambio)

**Responsabilidades:**
- porta `nombre`, `curso`, `caracter`, `estado` -- mostrados en la tabla plana de la variante Admin. Ya no colabora en la variante DirectorGrado (retirada de esta pantalla, sigue en [`abrirAsignaturasGrado()`](../abrirAsignaturasGrado/README.md)).

**Colaboraciones:**
- **Entrada:** listada por `AsignaturaGradoRepository`.

### `AsignaturaGradoRepository` (variante Admin, sin cambio)

**Responsabilidades:**
- lista las `AsignaturaGrado` de un `Grado` (`listarDelGrado(gradoId)`).

**Colaboraciones:**
- **Entrada:** `GradoController`.
- **Salida:** gestiona `AsignaturaGrado`.

## Simplificación fuera de alcance de esta rebanada

**`[Abrir]` por fila (variante Admin)**: la variante Admin de `abrirAsignaturaGrado()` no se construye en esta rebanada -- el botón se muestra deshabilitado.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirGrado/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirGrado/wireframes.puml) -- fuente de verdad del contenido presentado, ya divergido en dos bloques.
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `GRADOS_ABIERTO --> GRADO_ABIERTO : abrirGrado()`, y ahora también `GRADO_ABIERTO --> GUIA_ABIERTO : abrirGuia()` / `GRADO_ABIERTO --> GRADO_ABIERTO : notificarGuiasActualizadas()`.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `GRADOS_ABIERTO --> GRADO_ABIERTO : abrirGrado()`, `GRADO_ABIERTO --> GRADO_ABIERTO : crearAsignaturaGrado()/eliminarAsignaturaGrado()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Grado{codigo, estado}`, `Grado, Asignatura .. AsignaturaGrado`, `Guia` como clase de asociación de `(AsignaturaGrado, CursoAcademico)`.
- [`abrirGrados()`](../abrirGrados/README.md) -- listado del que se alcanza este caso de uso, en ambas variantes.
- [`abrirMaterias()`](../abrirMaterias/README.md) / [`abrirAsignaturaGrado()`](../abrirAsignaturaGrado/README.md) / [`abrirResultadosAprendizaje()`](../abrirResultadosAprendizaje/README.md) / [`abrirAsignaturasGrado()`](../abrirAsignaturasGrado/README.md) -- destinos hijos propios de `DirectorGrado`, alcanzados desde este mismo `GRADO_ABIERTO` sin necesitar mostrarse aquí (mismo criterio que `abrirMateria()` no muestra `SistemasEvaluacion`).
- [`crearAsignaturaGrado()`](../crearAsignaturaGrado/README.md) / [`eliminarAsignaturaGrado()`](../eliminarAsignaturaGrado/README.md) -- acciones exclusivas de la variante Admin, sin cambio.
- [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) -- colaboración origen del listado de `Guia` que esta variante DirectorGrado reutiliza; caso de uso propio sin fusionar.
- [`notificarGuiasActualizadas()`](../notificarGuiasActualizadas/README.md) -- alcanzado desde esta pantalla también, sin colaboración nueva (no se modela como arista en este diagrama, mismo criterio que `consultarEstadoGuias()` no la modela en el suyo).
- [PR #235](https://github.com/mmasias/pyCelda/pull/235) -- precedente del patrón de divergencia Admin/DirectorGrado aplicado aquí.
