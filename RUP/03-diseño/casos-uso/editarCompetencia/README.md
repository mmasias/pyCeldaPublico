<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarCompetencia() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarCompetencia/README.md)|[Análisis](/RUP/02-analisis/casos-uso/editarCompetencia/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-10-14
- **Autor**: Claude (vía Claude Code)

## Propósito

Bajada a diseño de [`editarCompetencia()`](/RUP/02-analisis/casos-uso/editarCompetencia/README.md): mismo esquema de validación que crear; el código propio no cuenta como repetido (`salvo_id`).

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/editarCompetencia/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EditarCompetencia` (React), prop `admin`.
- **API**: `routers/competencia.py::editar_competencia(competencia_id, datos)`.
- **Modelo**: `Competencia.actualizar(codigo, tipo, descripcion)`.
- **Repositorio**: `CompetenciaRepository.codigo_en_uso()`, `actualizar()`.

## Decisiones de diseño

- **Autorización compartida Admin/Director** (`routers/competencia.py::_puede_en_programa`): un mismo endpoint para los dos actores, sin espejo `/api/v1/admin/...`. Resuelve la identidad con `get_current_admin_email_opcional` y `get_current_director_programa_id_opcional`: con sesión Admin, cualquier `Programa`; sin ella, solo los que dirige el director. Fuera de eso, 404 uniforme, sin distinguir "no existe" de "no es tuyo" -- mismo criterio que los endpoints de programa de `ResultadoAprendizaje`.
- **`tipo` cerrado en el schema**, no en la base de datos: `TIPOS_COMPETENCIA` (`models/competencia.py`) es la única fuente; la columna es `VARCHAR(20)`, como el resto de enums del proyecto.
- **Unicidad doble**: el router responde 409 con mensaje legible; la restricción `UNIQUE (programa_id, codigo)` de la tabla queda como red de seguridad ante dos altas simultáneas.

## Referencias

- [`editarCompetencia()` en Análisis](/RUP/02-analisis/casos-uso/editarCompetencia/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarCompetencia/README.md).
