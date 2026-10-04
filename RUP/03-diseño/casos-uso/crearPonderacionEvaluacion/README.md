<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearPonderacionEvaluacion() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearPonderacionEvaluacion/README.md)|[Análisis](/RUP/02-analisis/casos-uso/crearPonderacionEvaluacion/README.md)|**Diseño**|[Desarrollo](/RUP/04-desarrollo/casos-uso/crearPonderacionEvaluacion/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-18
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`crearPonderacionEvaluacion()`](/RUP/02-analisis/casos-uso/crearPonderacionEvaluacion/README.md): CRUD real e inmediato contra `PonderacionEvaluacionRepository`, sin capa Service. Dos pasos -- cargar el selector de `SistemaEvaluacion` de la `Materia`, y crear -- con un único `<<choice>>`: el valor introducido, por sí solo, no puede superar `ponderacionMaxima` del `SistemaEvaluacion` elegido (`SistemaEvaluacion.validar_maximo()`, Fat Model). Sin comprobación contra la suma de hermanas ni contra el mínimo -- ambas son reglas agregadas de [`enviarGuiaARevision()`](/RUP/03-diseño/casos-uso/enviarGuiaARevision/README.md), no de aquí.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/crearPonderacionEvaluacion/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `CrearPonderacionEvaluacionView` (React) -- pide `GET /api/v1/materias/{materia_id}/sistemas-evaluacion` para el selector, y `POST /api/v1/guias/{guia_id}/ponderaciones-evaluacion` al confirmar.
- **API**: `routers/ponderacion_evaluacion.py::listar_sistemas_evaluacion(materia_id)` / `crear_ponderacion_evaluacion(guia_id, datos)` -- funciones sueltas, sin capa Service.
- **Modelo**: `Materia.listar_sistemas_evaluacion()` (relación ya cargada, sin lógica propia más allá de exponer la colección); `SistemaEvaluacion.validar_maximo(ponderacion)` (Fat Model: la regla del máximo puntual vive en la propia clase, no en el Router).
- **Repositorio**: `MateriaRepository.obtener(materia_id)`, `SistemaEvaluacionRepository.obtener(sistema_evaluacion_id)`, `PonderacionEvaluacionRepository.crear(guia_id, sistema_evaluacion_id, descripcion, ponderacion)`.

## Decisiones de diseño

- **Sin capa Service**: el Router llama a los repositorios y a los métodos de Modelo directamente -- decisión ya cerrada en la discussion [#58](https://github.com/mmasias/pyCelda/discussions/58).
- **`MateriaRepository` y `SistemaEvaluacionRepository`, ausentes en el diagrama de colaboración de Análisis**: ese nivel de abstracción no distingue el mecanismo de carga -- solo dice que `Materia`/`SistemaEvaluacion` responden a un método. Diseño sí necesita nombrar cómo llegan a memoria del proceso Python, así que cada uno recibe un repositorio mínimo de solo lectura (`obtener(id)`). No es una clase de Modelo nueva ni una regla de negocio -- es el mismo patrón de lectura que ya usa `GuiaRepository`.
- **La validación del máximo se repite en servidor** aunque el selector ya venga filtrado por `materia_id`: la petición de creación es un segundo request HTTP independiente (stateless) -- no hay garantía de que `sistema_evaluacion_id` siga siendo válido o que el cliente no lo haya alterado, así que `SistemaEvaluacion` se recarga y se revalida antes de crear.
- **`422 Unprocessable Entity`** en el rechazo, no `400 Bad Request` -- la petición está bien formada (los campos son correctos), lo que falla es una regla de negocio sobre su contenido.
- **La fila nace con `guia_id` pero sin vincular**, mismo mecanismo que [`crearReferenciaBibliografica()`](/RUP/03-diseño/casos-uso/crearReferenciaBibliografica/README.md) -- decisión 1 de la discussion [#58](https://github.com/mmasias/pyCelda/discussions/58).

## Referencias

- [`crearPonderacionEvaluacion()` en Análisis](/RUP/02-analisis/casos-uso/crearPonderacionEvaluacion/README.md) -- diagrama de colaboración origen, incluido el hallazgo sobre el panel de margen del wireframe.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearPonderacionEvaluacion/README.md).
- [`editarPonderacionEvaluacion()`](/RUP/03-diseño/casos-uso/editarPonderacionEvaluacion/README.md) -- misma validación de máximo puntual, mismo par `MateriaRepository`/`SistemaEvaluacionRepository`.
- Discussion [#58](https://github.com/mmasias/pyCelda/discussions/58) -- criterio de arranque de Diseño.
