<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > abrirMetodologiaDocente() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiaDocente/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirMetodologiaDocente/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-26
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`abrirMetodologiaDocente()`](/RUP/02-analisis/casos-uso/abrirMetodologiaDocente/README.md): un solo paso, de solo lectura. Presenta el `codigo` y la `descripcion` de la `MetodologiaDocente` -- los datos vienen de un único `GET` propio. A diferencia de `abrirUniversidad()`, no hay navegación a ningún catálogo hijo: `MetodologiaDocente` no compone nada, solo ofrece `[Editar]`/`[Volver al listado]`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirMetodologiaDocente/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AbrirMetodologiaDocenteView` (React) -- pide `GET /api/v1/metodologias-docentes/{metodologia_docente_id}`; presenta los dos datos y la navegación (`[Editar]`/`[Volver al listado]`).
- **API**: `routers/metodologia_docente.py::obtener_metodologia_docente(metodologia_docente_id)` -- función suelta.
- **Modelo**: ninguno con lógica propia invocada -- `MetodologiaDocente` solo porta los datos presentados.
- **Repositorio**: `MetodologiaDocenteRepository.obtener(metodologia_docente_id)` -- `SELECT` por clave primaria.

## Decisiones de diseño

- **`404` si el repositorio devuelve `None`**: guardia en la función del Router (`self.db.get()` de SQLAlchemy devuelve `None` por clave ausente) -- mismo mecanismo que el resto de `GET` por identificador del proyecto; no se modela como rama del diagrama porque desde el listado solo se alcanzan identificadores existentes.
- **Reutiliza el endpoint que `editarMetodologiaDocente()` usará como carga previa**: mismo `GET`, sin duplicar lógica de lectura.
- **Sin capa Service**: Router delgado -> Repository (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).
- **Autorización de `Admin`: `Depends(require_admin)`** -- toda función de `routers/metodologia_docente.py` la declara explícitamente; catálogo de `Admin` sin pertenencia que verificar (sin `get_current_director_grado_id`). El historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real, no un detalle menor.

## Referencias

- [`abrirMetodologiaDocente()` en Análisis](/RUP/02-analisis/casos-uso/abrirMetodologiaDocente/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiaDocente/README.md).
- [`abrirAsignatura()` en Diseño](/RUP/03-diseño/casos-uso/abrirAsignatura/README.md) -- precedente de `GET` de detalle de solo lectura.
- [`editarMetodologiaDocente()` en Diseño](/RUP/03-diseño/casos-uso/editarMetodologiaDocente/README.md) -- mismo endpoint `GET`, reutilizado como carga del formulario.
- [`abrirMetodologiasDocentes()` en Diseño](/RUP/03-diseño/casos-uso/abrirMetodologiasDocentes/README.md) -- listado desde el que se alcanza este caso de uso.
