<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > abrirGrados() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirGrados/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirGrados/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.1
- **Fecha**: 2026-08-24
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`abrirGrados()`](/RUP/02-analisis/casos-uso/abrirGrados/README.md), en sus dos variantes: la `DirectorGrado` (un solo paso, de solo lectura: el listado de `Grado` que dirige) y la `Admin` (listado del catálogo de una `Facultad`, con `[Abrir]`/`[Eliminar]` por fila y `[+ Crear Grado]`, construida junto a `crearGrado()`/`eliminarGrado()`). `GradoController` converge en `routers/grado.py`.

## Diagrama de secuencia de diseño

Este `secuencia.puml` contiene **dos diagramas**: el primero (`abrirGrados-diseño`) es la variante `DirectorGrado`; el segundo (`abrirGrados-admin-diseño`) es la variante `Admin`, anidada bajo `Facultad` -- mismo criterio de troceo que ya usa el proyecto para ficheros con más de un diagrama (`wireframes.puml` de Requisitos, `secuencia.puml` de `iniciarSesion()`).

<div align=center>

|`DirectorGrado` (variante real, `/api/v1/grados`)|`Admin` (variante anidada, `/api/v1/admin/facultades/{facultad_id}/grados`)|
|:-:|:-:|
|![](/images/RUP/03-diseño/casos-uso/abrirGrados/secuencia.svg)|![](/images/RUP/03-diseño/casos-uso/abrirGrados/secuencia-admin.svg)|
|<sup>Código fuente: [secuencia.puml](secuencia.puml)</sup>|<sup>mismo fichero, segundo bloque `@startuml`</sup>|

</div>

## Participantes

### Variante DirectorGrado

- **Vista**: `AbrirGradosView` (React) -- pide `GET /api/v1/grados`; presenta `codigo`, `nombre`, `estado` por fila.
- **API**: `routers/grado.py::listar_grados()` -- función suelta; el `director_grado_id` no llega por URL.
- **Modelo**: ninguno con lógica propia invocada -- `Grado` solo porta los datos de cada fila.
- **Repositorio**: `GradoRepository.listar_dirigidos_por(director_grado_id)` -- `SELECT` con join a la relación `Grado o- DirectorGrado` (agregación sin exclusividad: un director puede dirigir varios).

### Variante Admin

- **Vista**: `GradosAdmin.tsx` (React, ruta `/facultades/{facultad_id}/grados`) -- carga la `Facultad` para el título (`GRADOS -- <FACULTAD>`, tal cual el wireframe) y lista con `GET /api/v1/admin/facultades/{facultad_id}/grados`; `[Abrir]`/`[Eliminar]` por fila y `[+ Crear Grado]`.

  Nota (2026-08-30): `GradosAdmin.tsx` se fusionó con `Facultad.tsx` (discussion #149) -- la ruta pasó de `/facultades/{facultad_id}/grados` a `/facultades/{id}`.
- **API**: `routers/grado.py::listar_grados_de_la_facultad(facultad_id)` -- la `facultad_id` llega por URL, no por sesión.
- **Modelo**: ninguno con lógica propia invocada -- `Grado` solo porta los datos de cada fila (incluido `facultad_id` en `GradoResponse`).
- **Repositorio**: `GradoRepository.listar_de_la_facultad(facultad_id)` -- `SELECT` con `WHERE facultad_id = :facultad_id`.

## Decisiones de diseño

- **`director_grado_id` desde la sesión, no desde la URL** (variante `DirectorGrado`): la función del router lo recibe de la cookie de sesión (JWT, discussion [#62](https://github.com/mmasias/pyCelda/discussions/62)) -- es la variante `DirectorGrado` del CU compartido; `GET /api/v1/grados` sin parámetros devuelve solo lo que dirige quien llama.
- **Variante `Admin` anidada bajo `Facultad`, no listado global**: `GET /api/v1/admin/facultades/{facultad_id}/grados` con `Depends(require_admin)`. Corregido tras revisión en vivo de Manuel -- el wireframe real de `abrirGrados()` (`GRADOS -- ESCUELA POLITÉCNICA SUPERIOR`) y el Objetivo de `crearGrado()` ("en el catálogo de una Facultad") exigen listado/creación anidados bajo `Facultad`, no un listado global -- verificado contra el wireframe antes de corregir. El diseño original de PR #120 (`GET /api/v1/admin/grados` global, sin filtro) dejaba a cada `Grado` creado desde la UI huérfano de `Facultad` en la práctica.
- **Módulo `routers/grado.py` nuevo**: primera función de `Grado` en Diseño; el módulo crecerá con `obtener_grado()` (de `abrirGrado()`).
- **Sin capa Service**: Router delgado -> Repository, sin filtro post-consulta -- el filtrado (por director o por facultad) vive en el `WHERE`.

## Referencias

- [`abrirGrados()` en Análisis](/RUP/02-analisis/casos-uso/abrirGrados/README.md) -- diagrama de colaboración origen, con la simplificación de la variante `Admin`.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirGrados/README.md) -- fuente compartida con `Admin`, variante `wireframe-porDirector`.
- [`abrirGrado()` en Diseño](/RUP/03-diseño/casos-uso/abrirGrado/README.md) -- destino `[Abrir]` de cada fila.
