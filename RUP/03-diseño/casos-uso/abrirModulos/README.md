<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirModulos() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirModulos/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirModulos/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-10-14
- **Autor**: Claude (vía Claude Code)

## Propósito

Bajada a diseño de [`abrirModulos()`](/RUP/02-analisis/casos-uso/abrirModulos/README.md): listado y conteo agregado de materias, dos consultas.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirModulos/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `ModulosAdmin` (React), pestaña **🧱 Módulos** de `CabeceraProgramaAdmin`.
- **API**: `routers/modulo.py::listar_modulos_del_programa(programa_id)`.
- **Repositorio**: `ModuloRepository.listar_del_programa()`, `contar_materias_por_modulo()`.

## Decisiones de diseño

- **Solo Admin** (`require_admin`) para crear, editar y eliminar: rutas `/api/v1/admin/...`. El listado `GET /api/v1/programas/{programa_id}/modulos` admite también al director del `Programa` (lectura), con la misma autorización compartida que las competencias.
- **El mismo endpoint sirve al director**: las listas de materias de su vista lo usan para agrupar por módulo (solo lectura).

## Referencias

- [`abrirModulos()` en Análisis](/RUP/02-analisis/casos-uso/abrirModulos/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirModulos/README.md).
