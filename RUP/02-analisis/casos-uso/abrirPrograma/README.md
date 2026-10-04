<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirPrograma/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirPrograma/README.md), en sus dos variantes: un solo paso, sin `<<choice>>`, de solo lectura en ambas. La `Admin` es "la misma ficha" con más acciones: además de la tabla de `AsignaturaPrograma` (plana, con columna `Estado`, sin agrupar por `Materia`), ofrece el enlace "Ver Materias" (a [`abrirMaterias()`](../abrirMaterias/README.md)) y los botones `+ Crear AsignaturaPrograma` ([`crearAsignaturaPrograma()`](../crearAsignaturaPrograma/README.md)) y `[Eliminar]` por fila ([`eliminarAsignaturaPrograma()`](../eliminarAsignaturaPrograma/README.md)) -- ambos exclusivos de `Admin`. Sin cambio en este retoque.

**`DirectorPrograma` -- retocado (2026-09-05, Manuel usando el producto)**: presentaba los datos propios del `Programa` y sus `AsignaturaPrograma` agrupadas por `Materia`; pasa a presentar el listado de `Guia` del `Programa` -- mismas clases de colaboración que [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) (`listarGuiasDelPrograma(programaId)`/`GuiaRepository.listarDelPrograma(programaId)`), reutilizadas tal cual desde esta segunda pantalla. Motivo: la tabla de `AsignaturaPrograma` era un duplicado exacto de la propia pestaña [`abrirAsignaturasPrograma()`](../abrirAsignaturasPrograma/README.md) heredado del wireframe de `Admin`, sin enlace real a ninguna `Guia`. **Variante conservadora**: no se fusiona con `consultarEstadoGuias()` -- ambos casos de uso siguen siendo colaboraciones distintas, con sus propios diagramas, esta pantalla simplemente reutiliza el mismo par Controlador/Repositorio que aquel. Redundancia documental aceptada, no de código (mismo método real detrás de las dos pantallas).

Este `colaboracion.puml` contiene **dos diagramas**: el primero (`abrirPrograma-analisis`) es la variante `DirectorPrograma`; el segundo (`abrirPrograma-admin-analisis`) es la variante `Admin` -- mismo criterio de troceo que `secuencia.puml` de `iniciarSesion()` y de la variante Admin de [`abrirProgramas()`](../abrirProgramas/README.md).

<div align=center>

|`DirectorPrograma`|`Admin`|
|:-:|:-:|
|![](/images/RUP/02-analisis/casos-uso/abrirPrograma/colaboracion.svg)|![](/images/RUP/02-analisis/casos-uso/abrirPrograma/colaboracion-admin.svg)|
|<sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup>|<sup>mismo fichero, segundo bloque `@startuml`</sup>|

</div>

## Clases de vista

### `AbrirProgramaView`

**Responsabilidades (variante DirectorPrograma, retocada)**:
- presenta `codigo`, `nombre`, `estado` del `Programa`.
- presenta el listado de `Guia` del `Programa` (`AsignaturaPrograma`, profesorado, estado, última actualización) -- antes la tabla de `AsignaturaPrograma` agrupada por `Materia`, retirada de esta pantalla (sigue intacta en [`abrirAsignaturasPrograma()`](../abrirAsignaturasPrograma/README.md)).
- ofrece la navegación a abrir cada `Guia` ([`abrirGuia()`](../abrirGuia/README.md), reutilizado) y el botón `Notificar guías actualizadas` ([`notificarGuiasActualizadas()`](../notificarGuiasActualizadas/README.md), reutilizado) -- mismo contenido y mismas colaboraciones que [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md), duplicadas aquí a propósito.

**Responsabilidades (variante Admin):**
- presenta `codigo`, `nombre`, `estado` del `Programa`.
- presenta la tabla de `AsignaturaPrograma` (asignatura, materia, curso, carácter, estado) del `Programa`, con `[Abrir]` por fila deshabilitado en esta rebanada y `[Eliminar]` activo (navega a la confirmación de [`eliminarAsignaturaPrograma()`](../eliminarAsignaturaPrograma/README.md)).
- ofrece el enlace "Ver Materias" (a [`abrirMaterias()`](../abrirMaterias/README.md)), el botón `+ Crear AsignaturaPrograma` (a [`crearAsignaturaPrograma()`](../crearAsignaturaPrograma/README.md)), y la navegación a editar/eliminar el propio `Programa` y volver al listado de su `Facultad`.

**Colaboraciones:**
- **Entrada:** `:PROGRAMAS_ABIERTO` -- el `DirectorPrograma` o el `Admin` solicita abrir un `Programa`.
- **Control:** `ProgramaController`.
- **Salida:** `:PROGRAMA_ABIERTO`.

## Clases de controlador

### `ProgramaController`

**Responsabilidades (variante DirectorPrograma, retocada):**
- recupera el `Programa` (`cargarPrograma(programaId)`) para sus datos propios.
- lista las `Guia` del `Programa` (`listarGuiasDelPrograma(programaId)`) para el listado -- antes `listarAsignaturasPrograma(programaId)`; mismo método real que ya usaba `GuiaController` en [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md), reutilizado detrás de esta segunda Vista.

**Responsabilidades (variante Admin, sin cambio):**
- recupera el `Programa` (`cargarPrograma(programaId)`) para sus datos propios.
- lista las `AsignaturaPrograma` del `Programa` (`listarAsignaturasPrograma(programaId)`) para la tabla.

No valida ni muta nada en ninguna de las dos -- caso de uso de solo lectura en ambas variantes.

**Colaboraciones:**
- **Entrada:** `AbrirProgramaView`.
- **Salida (DirectorPrograma):** `ProgramaRepository`, `GuiaRepository`.
- **Salida (Admin):** `ProgramaRepository`, `AsignaturaProgramaRepository`.

## Clases de modelo

### `Programa`

**Responsabilidades:**
- porta `codigo` y `estado`.

**Colaboraciones:**
- **Entrada:** `ProgramaController`, vía `ProgramaRepository`.

### `ProgramaRepository`

**Responsabilidades:**
- recupera el `Programa` por identificador (`obtener(programaId)`).

**Colaboraciones:**
- **Entrada:** `ProgramaController`.
- **Salida:** gestiona `Programa`.

### `Guia` (variante DirectorPrograma, nueva en esta ficha)

**Responsabilidades:**
- porta `estado` y su `AsignaturaPrograma`/profesorado asociados -- mismas responsabilidades que documenta [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md), aquí mostradas desde una segunda Vista.

**Colaboraciones:**
- **Entrada:** listada por `GuiaRepository`.

### `GuiaRepository` (variante DirectorPrograma, nueva en esta ficha)

**Responsabilidades:**
- lista las `Guia` de un `Programa` (`listarDelPrograma(programaId)`) -- mismo método que ya existía para [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md), sin cambio de firma ni de comportamiento.

**Colaboraciones:**
- **Entrada:** `ProgramaController`.
- **Salida:** gestiona `Guia`.

### `AsignaturaPrograma` (variante Admin, sin cambio)

**Responsabilidades:**
- porta `nombre`, `curso`, `caracter`, `estado` -- mostrados en la tabla plana de la variante Admin. Ya no colabora en la variante DirectorPrograma (retirada de esta pantalla, sigue en [`abrirAsignaturasPrograma()`](../abrirAsignaturasPrograma/README.md)).

**Colaboraciones:**
- **Entrada:** listada por `AsignaturaProgramaRepository`.

### `AsignaturaProgramaRepository` (variante Admin, sin cambio)

**Responsabilidades:**
- lista las `AsignaturaPrograma` de un `Programa` (`listarDelPrograma(programaId)`).

**Colaboraciones:**
- **Entrada:** `ProgramaController`.
- **Salida:** gestiona `AsignaturaPrograma`.

## Simplificación fuera de alcance de esta rebanada

**`[Abrir]` por fila (variante Admin)**: la variante Admin de `abrirAsignaturaPrograma()` no se construye en esta rebanada -- el botón se muestra deshabilitado.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirPrograma/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirPrograma/wireframes.puml) -- fuente de verdad del contenido presentado, ya divergido en dos bloques.
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `PROGRAMAS_ABIERTO --> PROGRAMA_ABIERTO : abrirPrograma()`, y ahora también `PROGRAMA_ABIERTO --> GUIA_ABIERTO : abrirGuia()` / `PROGRAMA_ABIERTO --> PROGRAMA_ABIERTO : notificarGuiasActualizadas()`.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROGRAMAS_ABIERTO --> PROGRAMA_ABIERTO : abrirPrograma()`, `PROGRAMA_ABIERTO --> PROGRAMA_ABIERTO : crearAsignaturaPrograma()/eliminarAsignaturaPrograma()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa{codigo, estado}`, `Programa, Asignatura .. AsignaturaPrograma`, `Guia` como clase de asociación de `(AsignaturaPrograma, CursoAcademico)`.
- [`abrirProgramas()`](../abrirProgramas/README.md) -- listado del que se alcanza este caso de uso, en ambas variantes.
- [`abrirMaterias()`](../abrirMaterias/README.md) / [`abrirAsignaturaPrograma()`](../abrirAsignaturaPrograma/README.md) / [`abrirResultadosAprendizaje()`](../abrirResultadosAprendizaje/README.md) / [`abrirAsignaturasPrograma()`](../abrirAsignaturasPrograma/README.md) -- destinos hijos propios de `DirectorPrograma`, alcanzados desde este mismo `PROGRAMA_ABIERTO` sin necesitar mostrarse aquí (mismo criterio que `abrirMateria()` no muestra `SistemasEvaluacion`).
- [`crearAsignaturaPrograma()`](../crearAsignaturaPrograma/README.md) / [`eliminarAsignaturaPrograma()`](../eliminarAsignaturaPrograma/README.md) -- acciones exclusivas de la variante Admin, sin cambio.
- [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) -- colaboración origen del listado de `Guia` que esta variante DirectorPrograma reutiliza; caso de uso propio sin fusionar.
- [`notificarGuiasActualizadas()`](../notificarGuiasActualizadas/README.md) -- alcanzado desde esta pantalla también, sin colaboración nueva (no se modela como arista en este diagrama, mismo criterio que `consultarEstadoGuias()` no la modela en el suyo).
- [PR #235](https://github.com/mmasias/pyCelda/pull/235) -- precedente del patrón de divergencia Admin/DirectorPrograma aplicado aquí.
