<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > importarContenidoDeGuiaHermana() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/importarContenidoDeGuiaHermana/README.md)|[Análisis](/RUP/02-analisis/casos-uso/importarContenidoDeGuiaHermana/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-10-03
- **Autor**: Claude Sonnet 5.5 (vía Claude Code)

## Propósito

Bajada a diseño de [`importarContenidoDeGuiaHermana()`](/RUP/02-analisis/casos-uso/importarContenidoDeGuiaHermana/README.md) (issue [#409](https://github.com/mmasias/pyCelda/issues/409)): reutiliza **al completo** la infraestructura de [`importarBibliografiaDeGuiaHermana()`](/RUP/03-diseño/casos-uso/importarBibliografiaDeGuiaHermana/README.md) (issue [#184](https://github.com/mmasias/pyCelda/issues/184)) -- mismo router (`routers/importar_guia_hermana.py`), mismo `GET /api/v1/guias/{guia_id}/importables`, mismos helpers de autorización y de revalidación del origen, mismo schema de entrada -- y añade **un único endpoint**: `POST /api/v1/guias/{guia_id}/importar-contenido`. A diferencia de sus gemelos, no hay colección que reemplazar: el `contenido` es un campo escalar de la `Guia`, así que no interviene ningún repositorio de colección. Sin capa Service (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)): la función del router coordina repositorios y el Fat Model `Guia`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/importarContenidoDeGuiaHermana/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Endpoints

| Método | Ruta | Cuerpo | Respuesta | Autorización |
|-|-|-|-|-|
| `GET` | `/api/v1/guias/{guia_id}/importables` | -- | `list[GuiaHermanaImportableResponse]` | `get_current_profesor_id` + `imparte(destino.asignatura_programa_id, profesor_id)` -- reutilizado, ver [`importarBibliografiaDeGuiaHermana()`](/RUP/03-diseño/casos-uso/importarBibliografiaDeGuiaHermana/README.md) |
| `POST` | `/api/v1/guias/{guia_id}/importar-contenido` | `{origen_guia_id: int}` | `GuiaResponse` | ídem + revalidación de que `origen_guia_id` pertenece al conjunto de guías `Aprobada` de hermanas del curso activo |

Sin schema nuevo: se reutilizan `ImportarDeGuiaHermanaRequest` y `GuiaResponse`.

## Participantes

- **Vista (React)**: `ImportarContenidoDeGuiaHermanaView` -- **sin fichero ni ruta propios**: es un control inline en `AbrirGuia.tsx` (select de origen + botón "Importar contenido" tras el campo de texto de Contenido), alimentado por `listarGuiasImportables(guiaId)`. `importarContenido()` llama a `importarContenidoDeGuiaHermana(guiaId, origenGuiaId)` y asigna `respuesta.contenido` al estado local del campo de texto. No se ofrece en modo revisión ni si `listarGuiasImportables` no devuelve nada o falla (se trata como "sin importables").
- **API**: `routers/importar_guia_hermana.py::importar_contenido(guia_id, datos)` -- función suelta. Helpers compartidos: `_guia_destino_o_404()`, `_guias_hermanas_aprobadas()`, `_origen_o_404()`, `_identificador_origen()`, y el propio de este caso de uso, `_resumen_contenido()`.
- **Repositorios** (reutilizados de la familia #184, sin cambio): `AsignaturaProgramaRepository.imparte()` / `.listar_hermanas()`; `GuiaRepository.listar_aprobadas_de_asignaturas_programa(ids, curso_academico_id)`; `CursoAcademicoRepository.activo(universidad_id)`.
- **Modelo**:
  - `Guia.actualizar_contenido(contenido)` -- ya existente (lo usa también `guardarBorradorGuia()`); devuelve el valor anterior si el texto cambió, `None` si llega igual.
  - `Guia.confirmar_guardado()` -- reutilizado sin cambios: `fecha_ultima_modificacion = now()` y, si `estado == "Aprobada"`, `-> "Borrador"`.
  - `HistorialCambio.registrar(campo="contenido", ...)` -- una fila, **solo si hubo cambio**; `valor_anterior`/`valor_nuevo` = resumen corto del temario, `comentario = "contenido importado desde {programa} / {codigo}"`.

## Decisiones de diseño

- **Un solo commit por importación**, igual que bibliografía/planificación: el handler confirma una vez al final, tras `actualizar_contenido()` + `HistorialCambio` + `confirmar_guardado()`. Si algo falla, rollback completo.
- **Una fila de `HistorialCambio` solo si el contenido cambió**: `actualizar_contenido()` devuelve el valor anterior únicamente si el texto es distinto; importar un temario idéntico no genera fila ("no-op sin fila") -- el historial arranca con la primera acción humana real.
- **`confirmar_guardado()` se ejecuta siempre, haya o no cambio de contenido**: está fuera del `if` del Router, así que importar un temario idéntico sobre una guía `Aprobada` la degrada igualmente a `Borrador` y actualiza `fecha_ultima_modificacion`, aunque no quede fila de auditoría. Es el comportamiento implementado; documentado aquí para que no cambie en silencio.
- **`campo="contenido"` compartido con la edición manual**: no suma etiqueta nueva a la Auditoría de [`consultarHistorialCambios()`](/RUP/03-diseño/casos-uso/consultarHistorialCambios/README.md); a diferencia de `"bibliografia"`/`"planificacion_docente"`, que sí son campos propios de sus importaciones.
- **Resumen corto en `valor_anterior`/`valor_nuevo`**: el temario es texto largo y esas columnas son `String(50)`; `_resumen_contenido()` colapsa los espacios y trunca a 47 caracteres + `"..."`. El detalle completo del cambio no vive en la auditoría, vive en `Guia.contenido`. (`_resumen_contenido()` duplica la de `guia.py` -- es privada de ese módulo, no se importa cruzada.)
- **Revalidación server-side del origen y 404 uniforme**: el `origen_guia_id` del cliente nunca se confía; `_origen_o_404()` recalcula el conjunto de guías `Aprobada` de hermanas **del curso activo** y comprueba pertenencia -- mismo `"Guia no encontrada"` si el `Profesor` no imparte la guía destino que si el origen no es una hermana `Aprobada` válida. Sin selector de curso (issue [#443](https://github.com/mmasias/pyCelda/issues/443)): importar es una escritura, el abanico de orígenes es deliberadamente estrecho.
- **Reemplazo total, no fusión**: el `contenido` del destino se sustituye por completo por el del origen; la copia es de valor (texto), no un enlace -- editar luego el origen no afecta al destino.
- **Sin gate de estado en el destino**: igual que bibliografía, `_guia_destino_o_404()` solo comprueba que el `Profesor` imparte la guía, no su `estado`; importar sobre una guía `EnRevision` cambia el contenido sin degradarla (`confirmar_guardado()` solo actúa sobre `Aprobada`) -- idéntico a `guardarBorradorGuia()`. Familia [#219](https://github.com/mmasias/pyCelda/issues/219).
- **Deuda conocida, no arreglada aquí**: `confirmar_guardado()` no limpia `fecha_generacion_pdf` al degradar `Aprobada -> Borrador` -- comportamiento idéntico al pre-existente de `guardarBorradorGuia()`, familia [#219](https://github.com/mmasias/pyCelda/issues/219).
- **Punto crítico en la Vista**: el campo de texto de Contenido vive en estado local hasta `guardarBorradorGuia()`; sin asignar `respuesta.contenido` tras importar, un guardado posterior pisaría el contenido recién importado con el valor viejo que seguía en pantalla.
- **`GuiaResponse` (escalar), no `AbrirGuiaResponse`**: el `POST` devuelve solo los campos propios de la `Guia`, con el `estado` ya degradado.

## Referencias

- [`importarContenidoDeGuiaHermana()` en Análisis](/RUP/02-analisis/casos-uso/importarContenidoDeGuiaHermana/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/importarContenidoDeGuiaHermana/README.md).
- [`importarBibliografiaDeGuiaHermana()` en Diseño](/RUP/03-diseño/casos-uso/importarBibliografiaDeGuiaHermana/README.md) -- plantilla: mismo router, `GET` de importables y helpers.
- [`importarPlanificacionDocenteDeGuiaHermana()` en Diseño](/RUP/03-diseño/casos-uso/importarPlanificacionDocenteDeGuiaHermana/README.md) -- el otro gemelo de la familia #184.
- [`guardarBorradorGuia()` en Diseño](/RUP/03-diseño/casos-uso/guardarBorradorGuia/README.md) -- `actualizar_contenido()` y `confirmar_guardado()` reutilizados.
- [`abrirGuia()` en Diseño](/RUP/03-diseño/casos-uso/abrirGuia/README.md) -- pantalla que aloja el control inline.
- Discussion [#58](https://github.com/mmasias/pyCelda/discussions/58) -- sin capa Service.
