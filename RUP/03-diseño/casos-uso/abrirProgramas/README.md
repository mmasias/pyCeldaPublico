<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirProgramas() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirProgramas/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirProgramas/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.1
- **Fecha**: 2026-08-24
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`abrirProgramas()`](/RUP/02-analisis/casos-uso/abrirProgramas/README.md), en sus dos variantes: la `DirectorPrograma` (un solo paso, de solo lectura: el listado de `Programa` que dirige) y la `Admin` (listado del catálogo de una `Facultad`, con `[Abrir]`/`[Eliminar]` por fila y `[+ Crear Programa]`, construida junto a `crearPrograma()`/`eliminarPrograma()`). `ProgramaController` converge en `routers/programa.py`.

## Diagrama de secuencia de diseño

Este `secuencia.puml` contiene **dos diagramas**: el primero (`abrirProgramas-diseño`) es la variante `DirectorPrograma`; el segundo (`abrirProgramas-admin-diseño`) es la variante `Admin`, anidada bajo `Facultad` -- mismo criterio de troceo que ya usa el proyecto para ficheros con más de un diagrama (`wireframes.puml` de Requisitos, `secuencia.puml` de `iniciarSesion()`).

<div align=center>

|`DirectorPrograma` (variante real, `/api/v1/programas`)|`Admin` (variante anidada, `/api/v1/admin/facultades/{facultad_id}/programas`)|
|:-:|:-:|
|![](/images/RUP/03-diseño/casos-uso/abrirProgramas/secuencia.svg)|![](/images/RUP/03-diseño/casos-uso/abrirProgramas/secuencia-admin.svg)|
|<sup>Código fuente: [secuencia.puml](secuencia.puml)</sup>|<sup>mismo fichero, segundo bloque `@startuml`</sup>|

</div>

## Participantes

### Variante DirectorPrograma

- **Vista**: `AbrirProgramasView` (React) -- pide `GET /api/v1/programas`; presenta `codigo`, `nombre`, `estado` por fila.
- **API**: `routers/programa.py::listar_programas()` -- función suelta; el `director_programa_id` no llega por URL.
- **Modelo**: ninguno con lógica propia invocada -- `Programa` solo porta los datos de cada fila.
- **Repositorio**: `ProgramaRepository.listar_dirigidos_por(director_programa_id)` -- `SELECT` con join a la relación `Programa o- DirectorPrograma` (agregación sin exclusividad: un director puede dirigir varios).

### Variante Admin

- **Vista**: `ProgramasAdmin.tsx` (React, ruta `/facultades/{facultad_id}/programas`) -- carga la `Facultad` para el título (`PROGRAMAS -- <FACULTAD>`, tal cual el wireframe) y lista con `GET /api/v1/admin/facultades/{facultad_id}/programas`; `[Abrir]`/`[Eliminar]` por fila y `[+ Crear Programa]`.

  Nota (2026-08-30): `ProgramasAdmin.tsx` se fusionó con `Facultad.tsx` (discussion #149) -- la ruta pasó de `/facultades/{facultad_id}/programas` a `/facultades/{id}`.
- **API**: `routers/programa.py::listar_programas_de_la_facultad(facultad_id)` -- la `facultad_id` llega por URL, no por sesión.
- **Modelo**: ninguno con lógica propia invocada -- `Programa` solo porta los datos de cada fila (incluido `facultad_id` en `ProgramaResponse`).
- **Repositorio**: `ProgramaRepository.listar_de_la_facultad(facultad_id)` -- `SELECT` con `WHERE facultad_id = :facultad_id`.

## Decisiones de diseño

- **`director_programa_id` desde la sesión, no desde la URL** (variante `DirectorPrograma`): la función del router lo recibe de la cookie de sesión (JWT, discussion [#62](https://github.com/mmasias/pyCelda/discussions/62)) -- es la variante `DirectorPrograma` del CU compartido; `GET /api/v1/programas` sin parámetros devuelve solo lo que dirige quien llama.
- **Variante `Admin` anidada bajo `Facultad`, no listado global**: `GET /api/v1/admin/facultades/{facultad_id}/programas` con `Depends(require_admin)`. Corregido tras revisión en vivo de Manuel -- el wireframe real de `abrirProgramas()` (`PROGRAMAS -- ESCUELA POLITÉCNICA SUPERIOR`) y el Objetivo de `crearPrograma()` ("en el catálogo de una Facultad") exigen listado/creación anidados bajo `Facultad`, no un listado global -- verificado contra el wireframe antes de corregir. El diseño original de PR #120 (`GET /api/v1/admin/programas` global, sin filtro) dejaba a cada `Programa` creado desde la UI huérfano de `Facultad` en la práctica.
- **Módulo `routers/programa.py` nuevo**: primera función de `Programa` en Diseño; el módulo crecerá con `obtener_programa()` (de `abrirPrograma()`).
- **Sin capa Service**: Router delgado -> Repository, sin filtro post-consulta -- el filtrado (por director o por facultad) vive en el `WHERE`.

## Referencias

- [`abrirProgramas()` en Análisis](/RUP/02-analisis/casos-uso/abrirProgramas/README.md) -- diagrama de colaboración origen, con la simplificación de la variante `Admin`.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirProgramas/README.md) -- fuente compartida con `Admin`, variante `wireframe-porDirector`.
- [`abrirPrograma()` en Diseño](/RUP/03-diseño/casos-uso/abrirPrograma/README.md) -- destino `[Abrir]` de cada fila.
