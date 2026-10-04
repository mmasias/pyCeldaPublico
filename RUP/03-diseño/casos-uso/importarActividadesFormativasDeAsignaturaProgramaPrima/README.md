<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > importarActividadesFormativasDeAsignaturaProgramaPrima() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/importarActividadesFormativasDeAsignaturaProgramaPrima/README.md)|[Análisis](/RUP/02-analisis/casos-uso/importarActividadesFormativasDeAsignaturaProgramaPrima/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-10-03
- **Autor**: Claude Sonnet 5.5 (vía Claude Code)

## Propósito

Bajada a diseño de [`importarActividadesFormativasDeAsignaturaProgramaPrima()`](/RUP/02-analisis/casos-uso/importarActividadesFormativasDeAsignaturaProgramaPrima/README.md) (issues [#529](https://github.com/mmasias/pyCelda/issues/529) y [#530](https://github.com/mmasias/pyCelda/issues/530)). Primo del [`importarPlanificacionDocenteDeGuiaHermana()`](../importarPlanificacionDocenteDeGuiaHermana/README.md) de la familia [#184](https://github.com/mmasias/pyCelda/issues/184): mismo esquema "GET de candidatas + POST que reemplaza con revalidación server-side del origen", pero con diferencias de fondo: el origen no es una `Guia` aprobada sino una `AsignaturaPrograma` **prima** (misma `Materia`), el actor es `DirectorPrograma`, y el destino se **actualiza in place** (no borra y recrea), sin `HistorialCambio` ni efecto sobre ninguna `Guia`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/importarActividadesFormativasDeAsignaturaProgramaPrima/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EditarActividadesFormativasAsignaturaPrograma` (React, ruta `/asignaturas-programa/:id/actividades-formativas/editar`) -- la importación vive como sección "Importar de otra asignatura de la misma materia" de la pantalla de edición del reparto, no como pantalla propia. Tabla de primas (`nombre`, `ects` junto a los de la destino, `total_horas`) con un botón por fila; `window.confirm` previo del reemplazo total; estado vacío ("No hay asignaturas de la misma materia con actividades formativas configuradas") sin botones. Tras importar vuelve a la pantalla de origen.
- **API**: `routers/asignatura_programa.py` -- `listar_primas_importables_actividades_formativas(asignatura_programa_id)` (`GET .../actividades-formativas/importables`) e `importar_actividades_formativas_de_asignatura_programa_prima(asignatura_programa_id, datos)` (`POST .../actividades-formativas/importar`), con helper `_primas_importables(db, destino)` y auth `get_current_director_programa_id` + `_verificar_asignatura_programa_del_director`. Función suelta, sin capa Service ni `Controller`.
- **Modelo**: `ActividadFormativaAsignaturaPrograma.actualizar(horas, porcentaje_presencialidad)` -- la misma operación que usa [`editarActividadesFormativasAsignaturaPrograma()`](../editarActividadesFormativasAsignaturaPrograma/README.md).
- **Repositorios**: `AsignaturaProgramaRepository.obtener(id)` / `.listar_primas(asignatura_programa_id)`; `ActividadFormativaAsignaturaProgramaRepository.listar_de(asignatura_programa_id)` / `.guardar()`.

## Decisiones de diseño

- **Dos endpoints**: el `GET /importables` calcula las candidatas y el `POST /importar` las **recalcula** para validar el origen; el id que manda el cliente nunca se confía.
- **Primas = mismo `materia_id`**: `listar_primas` devuelve las otras `AsignaturaPrograma` de la misma `Materia`, excluyendo la propia (`[]` si el id no existe o la destino no tiene `materia_id`). A diferencia de `listar_hermanas()` (mismo `Asignatura` de catálogo, cualquier Materia/Programa), aquí el criterio es contenedor.
- **Candidatas**: solo primas con `sum(horas) > 0` (se excluyen las de 10 filas a 0); orden por `abs(ects_prima - ects_destino)` y luego por `nombre`.
- **`404` uniforme**: `AsignaturaPrograma` destino inexistente o no dirigida por el `DirectorPrograma` (`AsignaturaPrograma no encontrada`), y origen fuera del conjunto de candidatas -- inexistente, de otra Materia o sin configurar -- (`AsignaturaPrograma origen no encontrada`).
- **Reemplazo in place**: por cada fila de la destino se busca la fila del origen con el mismo `actividad_formativa_id` y se llama a `actualizar(horas, porcentaje_presencialidad)`; no se borra ni se crea nada. Un solo `guardar()` (commit) al final.
- **Sin `HistorialCambio` ni efecto en `Guia`**: el reparto de la `AsignaturaPrograma` no pasa por el historial de guías (a diferencia de `importarPlanificacionDocenteDeGuiaHermana()`).
- **Respuesta**: las 10 filas de la destino serializadas con `serializar_actividades_formativas_asignatura_programa`, misma forma que el `PUT` de edición.
- **Sin capa Service**: Router delgado -> Repository.

## Referencias

- [`importarActividadesFormativasDeAsignaturaProgramaPrima()` en Análisis](/RUP/02-analisis/casos-uso/importarActividadesFormativasDeAsignaturaProgramaPrima/README.md).
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/importarActividadesFormativasDeAsignaturaProgramaPrima/README.md).
- [`importarPlanificacionDocenteDeGuiaHermana()` en Diseño](../importarPlanificacionDocenteDeGuiaHermana/README.md) -- plantilla de formato (GET de candidatas + POST con revalidación).
- [`editarActividadesFormativasAsignaturaPrograma()` en Diseño](../editarActividadesFormativasAsignaturaPrograma/README.md) -- misma operación con valores tecleados.
