<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarMetodologiaDocente() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarMetodologiaDocente/README.md)|[Análisis](/RUP/02-analisis/casos-uso/editarMetodologiaDocente/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 2.0
- **Fecha**: 2026-10-17
- **Autor**: Claude (vía Claude Code)

## Propósito

Bajada a diseño de [`editarMetodologiaDocente()`](/RUP/02-analisis/casos-uso/editarMetodologiaDocente/README.md) (issue [#772](https://github.com/mmasias/pyCelda/issues/772)): mismo esquema de validación que crear; el código propio no cuenta como repetido (`salvo_id`).

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/editarMetodologiaDocente/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EditarMetodologiaDocente` (React), prop `admin`; campos en `FormularioCatalogoPrograma`.
- **API**: `routers/metodologia_docente.py::editar_metodologia_docente(metodologia_docente_id, datos)`.
- **Modelo**: `MetodologiaDocente.actualizar(codigo, descripcion)`.
- **Repositorio**: `MetodologiaDocenteRepository.codigo_en_uso()`, `actualizar()`.

## Decisiones de diseño

- **Autorización compartida Admin/Director** (`_autorizar_programa`/`_puede_en_programa`, importados de `routers/competencia.py`, y `_autorizar_metodologia` en `routers/metodologia_docente.py`): un mismo endpoint para los dos actores, sin espejo `/api/v1/admin/...`. Resuelve la identidad con `get_current_admin_email_opcional` y `get_current_director_programa_id_opcional`: con sesión Admin, cualquier `Programa`; sin ella, solo los que dirige el director. Fuera de eso, 404 uniforme, sin distinguir "no existe" de "no es tuyo" -- mismo criterio que `Competencia`.
- **Unicidad doble**: el router responde 409 con mensaje legible (`_rechazar_codigo_repetido()`, comparación con `UPPER` en las dos partes); la restricción `UNIQUE (programa_id, codigo)` de la tabla queda como red de seguridad ante dos peticiones simultáneas, y `_commit_o_409()` traduce el `IntegrityError` a 409, no a 500. La restricción de la tabla distingue mayúsculas; la comprobación previa, no.
- **`codigo` editable**: hasta #772 el formulario lo presentaba de solo lectura y lo reenviaba sin cambios.


## Referencias

- [`editarMetodologiaDocente()` en Análisis](/RUP/02-analisis/casos-uso/editarMetodologiaDocente/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarMetodologiaDocente/README.md).
