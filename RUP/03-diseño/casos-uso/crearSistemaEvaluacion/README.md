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

Bajada a diseño del caso de análisis [`crearSistemaEvaluacion()`](/RUP/02-analisis/casos-uso/crearSistemaEvaluacion/README.md): sin patrón C->U y sin `<<choice>>` -- los cinco campos (`codigo`, `tipo`, `descripcion`, `ponderacionMinima`, `ponderacionMaxima`) se piden de una vez y la creación es real e inmediata bajo la `Materia`. Un solo `POST` al Repository, sin método de Modelo intermedio ni rama de fallo de negocio.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/crearSistemaEvaluacion/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `CrearSistemaEvaluacion` (React, ruta `/admin/materias/:materiaId/sistemas-evaluacion/crear`) -- formulario con `codigo`, `tipo`, `descripcion`, `ponderacion_minima`, `ponderacion_maxima`; pide `POST /api/v1/materias/{materia_id}/sistemas-evaluacion` y navega al detalle de la creada.
- **API**: `routers/sistema_evaluacion.py::crear_sistema_evaluacion(materia_id, datos)` -- función suelta, sin capa Service.
- **Modelo**: ninguno con lógica propia invocada -- el `SistemaEvaluacion` nace con sus datos ya fijados; no hay invariante que proteger.
- **Repositorio**: `SistemaEvaluacionRepository.crear(materia_id, tipo, descripcion, ponderacion_minima, ponderacion_maxima, codigo)` -- `INSERT` inmediato con la FK al padre.

## Decisiones de diseño

- **Sin método de Modelo**: Análisis no introduce ningún `SistemaEvaluacion.crear()` ni validación de negocio -- el Repository construye la fila directamente (mismo criterio que `crearResultadoAprendizaje()`).
- **La obligatoriedad la resuelve Pydantic**: `SistemaEvaluacionCreate` (schemas/) exige `tipo`, `ponderacion_minima` y `ponderacion_maxima` antes de ejecutar la función del router; `descripcion` es opcional con default `""` y `codigo` opcional con default `None` (mismo patrón que `MetodologiaMateria.descripcion_propia`).
- **`tipo` es selector de lista fija, no texto libre**: el wireframe lo dibuja como dropdown (`^Evaluación continua^`) y el README de Requisitos lo fija explícitamente (`"Evaluación continua"`/`"Evaluación final"`, issue [#14](https://github.com/mmasias/pyCelda/issues/14)) -- normalizar este campo era justo el objetivo de esa issue al detallar `crearSistemaEvaluacion()`/`editarSistemaEvaluacion()` (las 63 variantes de texto libre del seed correspondían a `descripcion`, no a `tipo`). `SistemaEvaluacionCreate`/`Update` (schemas/) restringen `tipo` con `Literal["Evaluación continua", "Evaluación final"]`; la Vista lo presenta como `<select>` con esas dos opciones. `_canonical_sistema()` en `seed_programa.py` (que normaliza el texto libre histórico del seed hacia estos dos valores) es la prueba de que la lista cerrada ya era la intención real, no una simplificación nueva.
- **La coherencia del rango es validación de forma de la Vista**: `0 <= ponderacion_minima <= ponderacion_maxima <= 100` se comprueba en el formulario antes de enviar -- Requisitos no documenta ninguna invariante de negocio adicional y el backend no la exige (contraste: `validar_maximo()` sí es de negocio, pero vive en el hilo `PonderacionEvaluacion`).
- **`201 Created`**, mismo código que el resto de creaciones inmediatas.
- **`404` si la `Materia` no existe** -- guardia de Router sobre el `None` de `MateriaRepository.obtener()`: el alta cuelga de la composición, el padre debe existir.
- **Autorización de `Admin`: `Depends(require_admin)`**. *(superado por #755: `Admin` o `DirectorPrograma`, ver más abajo)*
- **Sin capa Service**: Router delgado -> Repository.

**Actor `DirectorPrograma` (issue [#755](https://github.com/mmasias/pyCelda/issues/755))**: mismo endpoint, que ahora admite los dos actores (`get_current_admin_email_opcional` + `get_current_director_programa_id_opcional`, helper `_autorizar_materia`): `Admin` sobre cualquier materia; el Director solo sobre las de sus programas (404 en otra, mismo criterio que `_verificar_materia_del_director`); ninguno de los dos, 403. Un path no admite dos guardas, de ahí el endpoint compartido, como `descargarGuiaPDF()`.

**Guarda de rango (issue [#755](https://github.com/mmasias/pyCelda/issues/755))**: crear un sistema o cambiar su rango se rechaza (409) si alguna `Guia` del curso activo En revisión o Aprobada de la `Materia` dejaría de cumplir la regla de `Guia.bloqueo_ponderaciones()` para ese sistema -- suma de sus `PonderacionEvaluacion` vinculadas en [mínima, máxima]; un sistema nuevo cuenta como 0 %. Las guías en Borrador o Rechazada no cuentan: se revalidan en `enviarGuiaARevision()`. Sin esta guarda, estrechar un rango invalidaba en silencio guías ya validadas.


**`codigo` (issue [#772](https://github.com/mmasias/pyCelda/issues/772))**: columna `sistemas_evaluacion.codigo VARCHAR(20) NULL` (esquema versión 4), el código de la memoria (p. ej. `E1`). En `_DatosSistemaEvaluacion` (base de `SistemaEvaluacionCreate`/`Update`) es `str | None`; un validador recorta espacios, aplica `validar_longitud(valor, 20, "El código")` y convierte el vacío en `None`. Sin unicidad: no hay restricción por `Materia` ni por `Programa`. `SistemaEvaluacionResponse` lo expone como `codigo: str | None`. `descripcion` no cambia de tipo; cambia su significado (denominación literal de la memoria).

## Referencias

- [`crearSistemaEvaluacion()` en Análisis](/RUP/02-analisis/casos-uso/crearSistemaEvaluacion/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearSistemaEvaluacion/README.md).
- [`crearResultadoAprendizaje()` en Diseño](/RUP/03-diseño/casos-uso/crearResultadoAprendizaje/README.md) -- precedente de alta anidada bajo un padre con los campos a la vez.
- [`editarSistemaEvaluacion()` en Diseño](/RUP/03-diseño/casos-uso/editarSistemaEvaluacion/README.md) -- edición disponible desde el detalle alcanzado.
