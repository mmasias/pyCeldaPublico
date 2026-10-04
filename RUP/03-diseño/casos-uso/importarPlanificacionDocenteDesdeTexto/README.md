<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > importarPlanificacionDocenteDesdeTexto() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/importarPlanificacionDocenteDesdeTexto/README.md)|[Análisis](/RUP/02-analisis/casos-uso/importarPlanificacionDocenteDesdeTexto/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-09-30
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño de [`importarPlanificacionDocenteDesdeTexto()`](/RUP/02-analisis/casos-uso/importarPlanificacionDocenteDesdeTexto/README.md) (issue [#552](https://github.com/mmasias/pyCelda/issues/552)). Hermano de [`importarPlanificacionDocenteDeGuiaHermana()`](../importarPlanificacionDocenteDeGuiaHermana/README.md): mismo router `importar_guia_hermana.py`, mismo `SesionRepository.reemplazar_desde`, mismo patrón de un-solo-commit, pero sin `GET /importables` ni hermandad -- el origen es el texto de la petición.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/importarPlanificacionDocenteDesdeTexto/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Específico del texto pegado

- **Endpoint**: `POST /api/v1/guias/{guia_id}/importar-planificacion-docente-desde-texto`, body `{texto: str}` (`ImportarPlanificacionDesdeTextoRequest`), respuesta `GuiaResponse`. `404` uniforme si la guía no existe o el `Profesor` no imparte su `AsignaturaPrograma` (`_guia_destino_o_404`).
- **Parser puro** `parsear_planificacion_texto(texto) -> list[tuple[str, str]]` (`core/parse_planificacion_texto.py`): sin acceso a datos. Por cada línea no vacía (`strip()`), `partition(" - ")` -- primera ocurrencia; código = parte izquierda con `strip()` + `upper()`, buscado en la tabla `CT/CP/CTP/CL/EC/EP`. Separador encontrado y código reconocido -> `(tipo, parte derecha.strip())`; separador encontrado y código no reconocido -> `("CLASE_TEORICA", línea completa)`. **Sin separador** (`rstrip("-")` + `strip()` sobre la línea, buscado igual en la tabla): código reconocido -> `(tipo, "")`, descripción vacía, el tipo no se descarta por falta de contenido; no reconocido -> `("CLASE_TEORICA", línea completa)` igual que el caso anterior. Corregido tras el primer despliegue (hallazgo de Manuel): el `strip()` de la línea completa se comía el espacio final del separador `" - "` cuando no había contenido, rompiendo el `partition()` exacto y descartando tipos válidos.
- **`SesionRepository.reemplazar_desde(destino, sesiones_transitorias)`**: las `Sesion` se construyen transitorias con `numero=1..N`, `vinculada=False`; el repositorio borra vía ORM las del destino y crea copias renumeradas 1..N en persistencia. No toca `Guia.sesiones_minimas`.
- **`HistorialCambio`**: `campo="planificacion_docente"`, `valor_anterior="{n} sesiones"`, `valor_nuevo="{m} sesiones (texto pegado)"`, `comentario="planificación docente importada desde texto pegado"`.
- **Guía `Aprobada`**: `confirmar_guardado()` la degrada a `Borrador`. **Texto vacío**: válido, deja la planificación vacía.
- **Vista**: `ImportarPlanificacionDocenteDesdeTexto.tsx` (ruta `/guias/:guiaId/importar-planificacion-docente-desde-texto`); botón en `PlanificacionDocente.tsx`; al confirmar, `limpiarExcluidos(claveSesionesExcluidas(guiaId))`.

## Referencias

- [`importarPlanificacionDocenteDesdeTexto()` en Análisis](/RUP/02-analisis/casos-uso/importarPlanificacionDocenteDesdeTexto/README.md).
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/importarPlanificacionDocenteDesdeTexto/README.md).
- [`importarPlanificacionDocenteDeGuiaHermana()` en Diseño](../importarPlanificacionDocenteDeGuiaHermana/README.md) -- mecánica compartida de reemplazo.
