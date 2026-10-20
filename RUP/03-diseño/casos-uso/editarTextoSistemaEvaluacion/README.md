<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarTextoSistemaEvaluacion() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarTextoSistemaEvaluacion/README.md)|[Análisis](/RUP/02-analisis/casos-uso/editarTextoSistemaEvaluacion/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 2.0
- **Fecha**: 2026-10-20
- **Autor**: Claude Sonnet 5.5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`editarTextoSistemaEvaluacion()`](/RUP/02-analisis/casos-uso/editarTextoSistemaEvaluacion/README.md) (issue [#791](https://github.com/mmasias/pyCelda/issues/791), antes [#610](https://github.com/mmasias/pyCelda/issues/610)): el Profesor elige la plantilla del texto de convocatorias del apartado 5 de la guía y rellena sus dos campos. Mismo patrón de edición simple que [`editarSistemaEvaluacion()`](../editarSistemaEvaluacion/README.md) (cargar por Repository, mutar, persistir), con validación de los tres datos (`422`) y la regla de estado común de las escrituras sobre la guía.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/editarTextoSistemaEvaluacion/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `PonderacionesEvaluacion` (React, ruta `/guias/:guiaId/ponderaciones-evaluacion`) -- selector de plantilla con las de `GET /api/v1/plantillas-evaluacion`, campos de instrumento y porcentaje si la plantilla los usa, propuesta (`instrumento_extraordinario_sugerido`, `porcentaje_recuperable_sugerido` del `GET` de la guía) con botón "Usar esta propuesta", aviso si el porcentaje no coincide con la suma de los instrumentos finales y texto resultante en solo lectura, compuesto en cliente con `textoConvocatorias.ts` para lo que aún no se ha guardado. Pide `PUT /api/v1/guias/{guia_id}/texto-sistema-evaluacion` con `{ plantilla, instrumento_extraordinario, porcentaje_recuperable }`.
- **API**: `routers/guia.py::editar_texto_sistema_evaluacion(guia_id, datos)` y `listar_plantillas_evaluacion()` -- funciones sueltas, sin capa Service. Autorización `get_current_rol` + `get_current_profesor_id_opcional` + `get_current_director_programa_id_opcional` y `autorizar_escritura_guia()`.
- **Modelo**: `models/plantilla_evaluacion.py` (las cinco plantillas, `plantilla_por_caracter()`, `componer_texto_convocatorias()`) y en `Guia`: columnas `plantilla_evaluacion` (atributo `plantilla_evaluacion_elegida`, NULL = la del carácter), `instrumento_extraordinario`, `porcentaje_recuperable`; propiedades `plantilla_evaluacion` (la aplicada), `texto_convocatorias`, `instrumento_extraordinario_sugerido`, `porcentaje_recuperable_sugerido`; método `bloqueo_convocatoria()` (regla `c4` de `enviarGuiaARevision()`).
- **Repositorios**: `GuiaRepository.obtener(guia_id)` / `.actualizar(guia)`; `AsignaturaProgramaRepository.imparte(asignatura_programa_id, profesor_id)`.

## Decisiones de diseño

- **El texto no se guarda**: se guardan la plantilla y los dos campos; el texto se compone en el modelo cada vez. La pantalla, la previsualización y el PDF usan `Guia.texto_convocatorias`, así que no pueden divergir. Las plantillas viven en el backend; la pantalla las pide para mostrar la que se elige antes de guardarla.
- **Plantilla elegida nullable**: NULL significa "la del carácter de la `AsignaturaPrograma`". Así las guías que nadie ha tocado siguen al carácter sin que la migración ni la creación de guías tengan que calcularla.
- **Validación en Router**: plantilla desconocida, instrumento de más de 300 caracteres, con saltos de línea o con alguno de los marcadores de la plantilla -> `422` (un marcador en el instrumento rompería la composición y el render); porcentaje fuera de 1-100 -> `422` del propio esquema (`Field(ge=1, le=100)`), que además acota el tamaño de `plantilla` y de `instrumento_extraordinario`. Nada se persiste si falla, ni cambia el estado. Con una plantilla sin campos, instrumento y porcentaje se guardan vacíos.
- **Plantilla desconocida en BD**: si la columna tiene un código que ya no existe, `Guia.plantilla_evaluacion` cae en la del carácter; la guía no deja de abrirse.
- **Propuestas guardables**: si la del instrumento pasa de 300 caracteres se queda en "las pruebas de evaluación final", sin los nombres; la del porcentaje es None si no cae en 1-100.
- **Guardar sin cambios no es una edición**: si plantilla aplicada, instrumento y porcentaje coinciden con los guardados, devuelve la guía sin tocarla ni su estado.
- **Regla de estado común** (`aplicar_regla_de_estado_por_escritura()`, #612, #707, #731): Director -> Aprobada pasa a Borrador y EnRevision a Rechazada; Profesor -> una Aprobada vuelve a Borrador (`confirmar_guardado()`). Admin queda fuera, como en el resto de escrituras sobre la guía.
- **Historial**: `HistorialCambio` `campo="plantilla_evaluacion"` con el autor real; valores "nombre de la plantilla; porcentaje; instrumento", resumidos a la longitud de la columna.
- **Propuestas**: los instrumentos vinculados de los sistemas de tipo "Evaluación final"; el instrumento se redacta como "la prueba de evaluación final (A)" o "las pruebas de evaluación final (A y B)", sin depender del género del nombre del instrumento; el porcentaje es su suma redondeada a entero. No se imponen: la regla de la convocatoria extraordinaria varía por programa.
- **Patrón B (clonado entre cursos)**: [`activarCursoAcademico()`](../activarCursoAcademico/README.md) copia la plantilla elegida y los dos campos de la `Guia` previa. No es parte de este flujo.
- **Sin capa Service**: Router delgado -> Repository.

## Referencias

- [`editarTextoSistemaEvaluacion()` en Análisis](/RUP/02-analisis/casos-uso/editarTextoSistemaEvaluacion/README.md).
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarTextoSistemaEvaluacion/README.md).
- [`editarSistemaEvaluacion()` en Diseño](../editarSistemaEvaluacion/README.md) -- plantilla de edición simple.
- [`activarCursoAcademico()` en Diseño](../activarCursoAcademico/README.md) -- clonado del texto entre cursos.
