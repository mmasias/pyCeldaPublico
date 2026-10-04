<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarAsociacionMetodologiaDocenteMateria() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarAsociacionMetodologiaDocenteMateria/README.md)|[Análisis](/RUP/02-analisis/casos-uso/editarAsociacionMetodologiaDocenteMateria/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-19
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`editarAsociacionMetodologiaDocenteMateria()`](/RUP/02-analisis/casos-uso/editarAsociacionMetodologiaDocenteMateria/README.md): sin `<<choice>>` -- edición del único campo propio de la clase de asociación, `descripcion_propia` (`codigo`/`descripcion` de la `MetodologiaDocente` se muestran en solo lectura). Dos interacciones de Análisis (`cargarAsociacion` + `guardarDescripcionPropia`) sobre la misma URL: `GET` + `PUT`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/editarAsociacionMetodologiaDocenteMateria/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EditarAsociacionMetodologiaDocenteMateriaView` (React) -- `codigo`/`descripcion` en solo lectura, `descripcion_propia` editable precargada; pide `GET` y `PUT /api/v1/materias/{materia_id}/metodologias-docentes/{metodologia_docente_id}`.
- **API**: `routers/materia.py::obtener_asociacion_metodologia_docente(materia_id, metodologia_docente_id)` / `::editar_asociacion_metodologia_docente(materia_id, metodologia_docente_id, datos)` -- funciones sueltas.
- **Modelo**: `MetodologiaMateria.actualizar(descripcion_propia)` -- único campo editable, patrón catálogo+override.
- **Repositorio**: `MetodologiaMateriaRepository.obtener(materia_id, metodologia_docente_id)` (clave compuesta) / `.actualizar(metodologia_materia)`.

## Decisiones de diseño

- **URL con clave compuesta (`{materia_id}` + `{metodologia_docente_id}`)**: `MetodologiaMateria` no tiene id propio en el modelo de dominio -- su identidad es el par; tanto el `GET` como el `PUT` y el `DELETE` de la desasociación usan la misma forma.
- **`MetodologiaMateriaUpdate` exige `descripcion_propia` presente**: el campo es editable y obligatorio en el formulario, aunque pueda enviarse como cadena vacía -- se distingue "no lo envías" (422) de "lo vacías" (válido).
- **Sin rama de fallo**: sin `<<choice>>` en Análisis ni validación de negocio -- camino único de guardado.

## Referencias

- [`editarAsociacionMetodologiaDocenteMateria()` en Análisis](/RUP/02-analisis/casos-uso/editarAsociacionMetodologiaDocenteMateria/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarAsociacionMetodologiaDocenteMateria/README.md).
- [`asociarMetodologiaDocenteAMateria()` en Diseño](/RUP/03-diseño/casos-uso/asociarMetodologiaDocenteAMateria/README.md) -- quien crea la asociación con `descripcion_propia` vacía.
