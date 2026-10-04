<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearSistemaEvaluacion() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearSistemaEvaluacion/README.md)|[Análisis](/RUP/02-analisis/casos-uso/crearSistemaEvaluacion/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-26
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`crearSistemaEvaluacion()`](/RUP/02-analisis/casos-uso/crearSistemaEvaluacion/README.md): sin patrón C->U y sin `<<choice>>` -- los cuatro campos (`tipo`, `descripcion`, `ponderacionMinima`, `ponderacionMaxima`) se piden de una vez y la creación es real e inmediata bajo la `Materia`. Un solo `POST` al Repository, sin método de Modelo intermedio ni rama de fallo de negocio.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/crearSistemaEvaluacion/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `CrearSistemaEvaluacion` (React, ruta `/admin/materias/:materiaId/sistemas-evaluacion/crear`) -- formulario con `tipo`, `descripcion`, `ponderacion_minima`, `ponderacion_maxima`; pide `POST /api/v1/materias/{materia_id}/sistemas-evaluacion` y navega al detalle de la creada.
- **API**: `routers/sistema_evaluacion.py::crear_sistema_evaluacion(materia_id, datos)` -- función suelta, sin capa Service.
- **Modelo**: ninguno con lógica propia invocada -- el `SistemaEvaluacion` nace con los cuatro datos ya fijados; no hay invariante que proteger.
- **Repositorio**: `SistemaEvaluacionRepository.crear(materia_id, tipo, descripcion, ponderacion_minima, ponderacion_maxima)` -- `INSERT` inmediato con la FK al padre.

## Decisiones de diseño

- **Sin método de Modelo**: Análisis no introduce ningún `SistemaEvaluacion.crear()` ni validación de negocio -- el Repository construye la fila directamente (mismo criterio que `crearResultadoAprendizaje()`).
- **La obligatoriedad la resuelve Pydantic**: `SistemaEvaluacionCreate` (schemas/) exige `tipo`, `ponderacion_minima` y `ponderacion_maxima` antes de ejecutar la función del router; `descripcion` es opcional con default `""` (mismo patrón que `MetodologiaMateria.descripcion_propia`).
- **`tipo` es selector de lista fija, no texto libre**: el wireframe lo dibuja como dropdown (`^Evaluación continua^`) y el README de Requisitos lo fija explícitamente (`"Evaluación continua"`/`"Evaluación final"`, issue [#14](https://github.com/mmasias/pyCelda/issues/14)) -- normalizar este campo era justo el objetivo de esa issue al detallar `crearSistemaEvaluacion()`/`editarSistemaEvaluacion()` (las 63 variantes de texto libre del seed correspondían a `descripcion`, no a `tipo`). `SistemaEvaluacionCreate`/`Update` (schemas/) restringen `tipo` con `Literal["Evaluación continua", "Evaluación final"]`; la Vista lo presenta como `<select>` con esas dos opciones. `_canonical_sistema()` en `seed_programa.py` (que normaliza el texto libre histórico del seed hacia estos dos valores) es la prueba de que la lista cerrada ya era la intención real, no una simplificación nueva.
- **La coherencia del rango es validación de forma de la Vista**: `0 <= ponderacion_minima <= ponderacion_maxima <= 100` se comprueba en el formulario antes de enviar -- Requisitos no documenta ninguna invariante de negocio adicional y el backend no la exige (contraste: `validar_maximo()` sí es de negocio, pero vive en el hilo `PonderacionEvaluacion`).
- **`201 Created`**, mismo código que el resto de creaciones inmediatas.
- **`404` si la `Materia` no existe** -- guardia de Router sobre el `None` de `MateriaRepository.obtener()`: el alta cuelga de la composición, el padre debe existir.
- **Autorización de `Admin`: `Depends(require_admin)`**.
- **Sin capa Service**: Router delgado -> Repository.

## Referencias

- [`crearSistemaEvaluacion()` en Análisis](/RUP/02-analisis/casos-uso/crearSistemaEvaluacion/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearSistemaEvaluacion/README.md).
- [`crearResultadoAprendizaje()` en Diseño](/RUP/03-diseño/casos-uso/crearResultadoAprendizaje/README.md) -- precedente de alta anidada bajo un padre con los campos a la vez.
- [`editarSistemaEvaluacion()` en Diseño](/RUP/03-diseño/casos-uso/editarSistemaEvaluacion/README.md) -- edición disponible desde el detalle alcanzado.
