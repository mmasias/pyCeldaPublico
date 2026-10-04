<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirMaterias() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirMaterias/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirMaterias/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.1
- **Fecha**: 2026-08-25
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`abrirMaterias()`](/RUP/02-analisis/casos-uso/abrirMaterias/README.md), en sus dos variantes: la `DirectorPrograma` (un solo paso, de solo lectura: punto de partida de los casos de asociación) y la `Admin` (mismo listado alcanzado desde el enlace "Ver Materias" de la ficha del `Programa`, con `[Abrir]`/`[Eliminar]` por fila y `+ Crear Materia`, construida junto a `crearMateria()` en el lote de Materia/AsignaturaPrograma). Ambas convergen en el mismo `MateriaRepository.listar_del_programa()`.

Este `secuencia.puml` contiene **dos diagramas**: el primero (`abrirMaterias-diseño`) es la variante `DirectorPrograma`; el segundo (`abrirMaterias-admin-diseño`) es la variante `Admin` -- mismo criterio de troceo que `secuencia.puml` de `iniciarSesion()` y de la variante Admin de [`abrirProgramas()`](../abrirProgramas/README.md).

## Diagrama de secuencia de diseño

<div align=center>

|`DirectorPrograma` (`/api/v1/programas/{programa_id}/materias`)|`Admin` (`/api/v1/admin/programas/{programa_id}/materias`)|
|:-:|:-:|
|![](/images/RUP/03-diseño/casos-uso/abrirMaterias/secuencia.svg)|![](/images/RUP/03-diseño/casos-uso/abrirMaterias/secuencia-admin.svg)|
|<sup>Código fuente: [secuencia.puml](secuencia.puml)</sup>|<sup>mismo fichero, segundo bloque `@startuml`</sup>|

</div>

## Participantes

### Variante DirectorPrograma

- **Vista**: `AbrirMateriasView` (React) -- pide `GET /api/v1/programas/{programa_id}/materias`; presenta `nombre` por fila.
- **API**: `routers/materia.py::listar_materias_del_programa(programa_id)` -- función suelta; guard de `DirectorPrograma`.
- **Modelo**: ninguno con lógica propia invocada -- `Materia` porta el dato de cada fila.
- **Repositorio**: `MateriaRepository.listar_del_programa(programa_id)`.

### Variante Admin

- **Vista**: `MateriasAdmin.tsx` (React, ruta `/admin/programas/{programa_id}/materias`) -- lista con `GET /api/v1/admin/programas/{programa_id}/materias`; `[Abrir]` por fila (a `MateriaAdmin.tsx`), `[Eliminar]` deshabilitado (`eliminarMateria()` fuera de esta rebanada) y `+ Crear Materia` (a `CrearMateriaAdmin.tsx`).
- **API**: `routers/materia.py::listar_materias_admin(programa_id)` -- la `programa_id` llega por URL, guard `Depends(require_admin)`.
- **Modelo**: ninguno con lógica propia invocada -- `Materia` porta el dato de cada fila (incluido `programa_id` en `MateriaResponse`).
- **Repositorio**: `MateriaRepository.listar_del_programa(programa_id)` -- reutilizado tal cual: la variante Admin no añade ningún método nuevo de lectura, solo el namespace de autorización.

## Decisiones de diseño

- **Ruta anidada bajo `/programas/{programa_id}` en ambas variantes**: `Programa *-- Materia` es composición -- se navega desde dentro del `Programa` abierto, no como catálogo institucional plano; la URL refleja la jerarquía.
- **Namespace Admin separado, mismo repositorio**: `GET /api/v1/admin/programas/{programa_id}/materias` con `Depends(require_admin)` junto al `GET /api/v1/programas/{programa_id}/materias` con `Depends(get_current_director_programa_id)` -- mismo criterio que separó los dos `abrirProgramas()`; el `SELECT` es idéntico (`WHERE programa_id = :programa_id`).
- **`[Eliminar]` deshabilitado en la variante Admin**: el wireframe lo ofrece, pero `eliminarMateria()` no forma parte de esta rebanada -- el botón se renderiza con `title="Fuera de alcance de esta rebanada"` para no desviar el wireframe.
- **Sin capa Service**: Router delgado -> Repository, sin filtro post-consulta.

## Referencias

- [`abrirMaterias()` en Análisis](/RUP/02-analisis/casos-uso/abrirMaterias/README.md) -- diagrama de colaboración origen, con ambas variantes.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirMaterias/README.md) -- fuente compartida por ambos actores.
- [`abrirMateria()` en Diseño](/RUP/03-diseño/casos-uso/abrirMateria/README.md) -- destino `[Abrir]` de cada fila, con su variante Admin construida en este mismo lote.
- [`crearMateria()` en Diseño](/RUP/03-diseño/casos-uso/crearMateria/README.md) -- acción `+ Crear Materia` de la variante Admin, construida en este mismo lote.
- [`abrirProgramas()` en Diseño](/RUP/03-diseño/casos-uso/abrirProgramas/README.md) -- precedente del troceo multi-diagrama por variante de actor.
