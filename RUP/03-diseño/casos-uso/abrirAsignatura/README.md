<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > abrirAsignatura() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignatura/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirAsignatura/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-24
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`abrirAsignatura()`](/RUP/02-analisis/casos-uso/abrirAsignatura/README.md): un solo paso, de solo lectura. Presenta el `nombre`, los `ects`, el `estado` y el `contenido` de la `Asignatura` -- los datos vienen de un único `GET` propio. A diferencia de `abrirUniversidad()`, no hay navegación a ningún catálogo hijo: `Asignatura` no compone nada, solo ofrece `[Editar]`/`[Volver al listado]`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirAsignatura/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AbrirAsignaturaView` (React) -- pide `GET /api/v1/asignaturas/{asignatura_id}`; presenta los cuatro datos y la navegación (`[Editar]`/`[Volver al listado]`).
- **API**: `routers/asignatura.py::obtener_asignatura(asignatura_id)` -- función suelta.
- **Modelo**: ninguno con lógica propia invocada -- `Asignatura` solo porta los datos presentados.
- **Repositorio**: `AsignaturaRepository.obtener(asignatura_id)` -- `SELECT` por clave primaria.

## Decisiones de diseño

- **`404` si el repositorio devuelve `None`**: guardia en la función del Router (`self.db.get()` de SQLAlchemy devuelve `None` por clave ausente) -- mismo mecanismo que el resto de `GET` por identificador del proyecto; no se modela como rama del diagrama porque desde el listado solo se alcanzan identificadores existentes.
- **Reutiliza el endpoint que `editarAsignatura()` usará como carga previa**: mismo `GET`, sin duplicar lógica de lectura.
- **Sin capa Service**: Router delgado -> Repository (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).
- **Autorización de `Admin`: `Depends(require_admin)`** -- ya disponible en `backend/app/core/auth.py` (bloque anterior, ya mergeado), sin nota de pendiente: toda función de `routers/asignatura.py` la declara explícitamente. El historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real, no un detalle menor.

## Referencias

- [`abrirAsignatura()` en Análisis](/RUP/02-analisis/casos-uso/abrirAsignatura/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignatura/README.md).
- [`abrirUniversidad()` en Diseño](/RUP/03-diseño/casos-uso/abrirUniversidad/README.md) -- precedente de `GET` de detalle de solo lectura.
- [`editarAsignatura()` en Diseño](/RUP/03-diseño/casos-uso/editarAsignatura/README.md) -- mismo endpoint `GET`, reutilizado como carga del formulario.
- [`abrirAsignaturas()` en Diseño](/RUP/03-diseño/casos-uso/abrirAsignaturas/README.md) -- listado desde el que se alcanza este caso de uso.
