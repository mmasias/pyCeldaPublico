<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearModulo() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearModulo/README.md)|[Análisis](/RUP/02-analisis/casos-uso/crearModulo/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-10-14
- **Autor**: Claude (vía Claude Code)

## Propósito

Bajada a diseño de [`crearModulo()`](/RUP/02-analisis/casos-uso/crearModulo/README.md): validación de forma en el schema (422) y de código repetido en el router (409, con `UNIQUE (programa_id, codigo)` como red de seguridad).

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/crearModulo/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `CrearModuloAdmin` (React).
- **API**: `routers/modulo.py::crear_modulo(programa_id, datos)`.
- **Schema**: `ModuloCreate` (`_DatosModulo`).
- **Repositorio**: `ModuloRepository.codigo_en_uso()`, `crear()`.

## Decisiones de diseño

- **Solo Admin** (`require_admin`) para crear, editar y eliminar: rutas `/api/v1/admin/...`. El listado `GET /api/v1/programas/{programa_id}/modulos` admite también al director del `Programa` (lectura), con la misma autorización compartida que las competencias.
- **Descripción opcional**: el schema la recorta y la columna la guarda como cadena vacía, no `NULL`.

## Referencias

- [`crearModulo()` en Análisis](/RUP/02-analisis/casos-uso/crearModulo/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearModulo/README.md).
