<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > abrirUniversidad() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirUniversidad/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirUniversidad/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-24
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`abrirUniversidad()`](/RUP/02-analisis/casos-uso/abrirUniversidad/README.md): un solo paso, de solo lectura. Presenta el `nombre` de la `Universidad` y ofrece la navegación a sus `Facultad` -- los datos vienen de un único `GET` propio; la pantalla de `Facultad` es otro CU ([`abrirFacultades()`](/RUP/03-diseño/casos-uso/abrirFacultades/README.md)), no una segunda consulta de este.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirUniversidad/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AbrirUniversidadView` (React) -- pide `GET /api/v1/universidades/{universidad_id}`; presenta `nombre` y la navegación (`[Editar]`/`[Ver Facultades]`/`[Volver al listado]`).
- **API**: `routers/universidad.py::obtener_universidad(universidad_id)` -- función suelta.
- **Modelo**: ninguno con lógica propia invocada -- `Universidad` solo porta los datos presentados.
- **Repositorio**: `UniversidadRepository.obtener(universidad_id)` -- `SELECT` por clave primaria.

## Decisiones de diseño

- **`404` si el repositorio devuelve `None`**: guardia en la función del Router (`self.db.get()` de SQLAlchemy devuelve `None` por clave ausente) -- mismo mecanismo que el resto de `GET` por identificador del proyecto; no se modela como rama del diagrama porque desde el listado solo se alcanzan identificadores existentes.
- **Reutiliza el endpoint que `editarUniversidad()` usará como carga previa**: mismo `GET`, sin duplicar lógica de lectura.
- **Sin capa Service**: Router delgado -> Repository (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).
- **Autorización de `Admin`: `Depends(require_admin)`** (dependencia fijada en el diseño de [`iniciarSesion()`](/RUP/03-diseño/casos-uso/iniciarSesion/README.md), no implementada en este documento) -- toda función de `routers/universidad.py` debe declararla explícitamente en Desarrollo. El historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real, no un detalle menor.

## Referencias

- [`abrirUniversidad()` en Análisis](/RUP/02-analisis/casos-uso/abrirUniversidad/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirUniversidad/README.md).
- [`abrirGrado()` en Diseño](/RUP/03-diseño/casos-uso/abrirGrado/README.md) -- precedente de `GET` de detalle de solo lectura.
- [`editarUniversidad()` en Diseño](/RUP/03-diseño/casos-uso/editarUniversidad/README.md) -- mismo endpoint `GET`, reutilizado como carga del formulario.
- [`abrirFacultades()` en Diseño](/RUP/03-diseño/casos-uso/abrirFacultades/README.md) -- destino del botón `[Ver Facultades]`.
