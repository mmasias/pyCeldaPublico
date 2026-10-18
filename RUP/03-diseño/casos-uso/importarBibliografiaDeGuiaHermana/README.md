<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > importarBibliografiaDeGuiaHermana() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/importarBibliografiaDeGuiaHermana/README.md)|[Análisis](/RUP/02-analisis/casos-uso/importarBibliografiaDeGuiaHermana/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-09-05
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño de [`importarBibliografiaDeGuiaHermana()`](/RUP/02-analisis/casos-uso/importarBibliografiaDeGuiaHermana/README.md) (issue [#184](https://github.com/mmasias/pyCelda/issues/184)). Dos endpoints: un `GET` para listar orígenes candidatos y un `POST` que ejecuta la copia con reemplazo total. Sin capa Service (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)): las funciones del router coordinan repositorios y el Fat Model `Guia`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/importarBibliografiaDeGuiaHermana/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Endpoints

| Método | Ruta | Cuerpo | Respuesta | Autorización |
|-|-|-|-|-|
| `GET` | `/api/v1/guias/{guia_id}/importables` | -- | `list[GuiaHermanaImportableResponse]` | `get_current_profesor_id` + `imparte(destino.asignatura_programa_id, profesor_id)` |
| `POST` | `/api/v1/guias/{guia_id}/importar-bibliografia` | `{origen_guia_id: int}` | `GuiaResponse` | ídem + revalidación de que `origen_guia_id` pertenece al conjunto de guías importables de hermanas (`Aprobada`, o `EnRevision` que el profesor también imparte; issue [#740](https://github.com/mmasias/pyCelda/issues/740)) |
| `POST` | `/api/v1/guias/{guia_id}/importar-planificacion-docente` | `{origen_guia_id: int}` | `GuiaResponse` | ídem (endpoint gemelo, ver [`importarPlanificacionDocenteDeGuiaHermana()`](../importarPlanificacionDocenteDeGuiaHermana/README.md)) |

`GuiaHermanaImportableResponse = {guia_id, programa_codigo, asignatura_codigo, asignatura_programa_nombre, estado: str, fecha_estado: datetime | None, n_referencias, n_sesiones}` -- `estado` es `"Aprobada"` o `"EnRevision"`; `estado` + `fecha_estado` sustituyen al antiguo `fecha_aprobacion` (issue #740). El `GET` devuelve los tres campos de ambos CU (`n_referencias` y `n_sesiones`) en la misma respuesta -- un único punto de relajación de la regla de autorización, no dos.

Router propio: `backend/app/routers/importar_guia_hermana.py` (registrado en `main.py` junto a `sesion.router`). Schema propio: `backend/app/schemas/importar_guia_hermana.py`.

## Participantes

- **Vista (React)**: `ImportarBibliografiaDeGuiaHermana.tsx` (ruta `/guias/:guiaId/importar-bibliografia`) -- desplegable de orígenes (`listarGuiasImportables`) + aviso del recuento a reemplazar; cada opción rotula el estado del origen con `textoEstadoHermana()` ("aprobada el dd/mm/aaaa" o "en revisión desde dd/mm/aaaa") y la lista vacía muestra `SIN_HERMANAS_IMPORTABLES`, ambos de `frontend/src/guiaHermana.ts`, compartidos por los tres casos de uso de la familia; al confirmar, `importarBibliografiaDeGuiaHermana(guiaId, origenGuiaId)` y `limpiarExcluidos(claveReferenciasExcluidas(guiaId))` (los ids de la lista de trabajo en `sessionStorage` apuntan a filas ya borradas). El botón `[Importar de asignatura hermana]` vive en `ReferenciasBibliograficas.tsx`, condicional a que `listarGuiasImportables` devuelva algo.
- **API**: `routers/importar_guia_hermana.py` -- `listar_importables()`, `importar_bibliografia()`. Helpers: `_guia_destino_o_404()`, `_guias_hermanas_importables(db, guia_destino, profesor_id)`, `_origen_o_404(db, destino, origen_guia_id, profesor_id)`, `_fecha_estado()`, `_registrar_importacion()`.
- **Repositorios**:
  - `AsignaturaProgramaRepository.listar_hermanas(asignatura_programa_id)` -- join a `Asignatura`, `asignatura_id ==` Y `Asignatura.codigo ==`, `id !=`; `[]` si `asignatura_id IS NULL` o el catálogo no tiene código.
  - `AsignaturaProgramaRepository.imparte(asignatura_programa_id, profesor_id)` -- además de autorizar el destino, filtra las candidatas `EnRevision`: `_guias_hermanas_importables()` solo conserva una `EnRevision` si el profesor también imparte su `AsignaturaPrograma`.
  - `GuiaRepository.listar_importables_de_asignaturas_programa(ids, curso_academico_id)` -- filtra `estado IN ("Aprobada", "EnRevision")` y el `CursoAcademico` activo (el filtro de "imparte" de las `EnRevision` no está en esta consulta, lo aplica el router), precarga `referencias`/`sesiones`/`historial`/`asignatura_programa.asignatura`.
  - `ReferenciaBibliograficaRepository.reemplazar_desde(guia_destino, referencias_origen)` -- borra vía ORM la colección ya cargada del destino, crea copias (`tipo`, `referencia`, `vinculada` replicada fila a fila), `flush()` sin `commit`.
- **Modelo**:
  - `AsignaturaPrograma.asignatura` -- relación many-to-one nueva hacia `Asignatura` (solo lectura, la necesita `listar_hermanas` y el código del origen). No añade columna: `asignatura_id` ya existe desde #181.
  - `Guia.confirmar_guardado()` -- reutilizado sin cambios: `fecha_ultima_modificacion = now()` y, si `estado == "Aprobada"`, `-> "Borrador"`.
  - `HistorialCambio.registrar(campo="bibliografia", ...)` -- una fila; `valor_anterior = "{n} referencias"`, `valor_nuevo = "{programa} / {codigo}"`, `comentario = "bibliografía importada desde {programa} / {codigo}"`.

## Decisiones de diseño

- **Un solo commit por importación**. Las llamadas a repo (`reemplazar_desde`) hacen `flush()`, no `commit()` -- excepción documentada al patrón habitual del proyecto (donde cada método de repo confirma). El handler confirma una vez al final, tras `reemplazar_desde` + `HistorialCambio` + `confirmar_guardado()`. Si algo falla, rollback completo (atomicidad de la regla D6 del hilo #184).
- **Borrado vía ORM, no `bulk delete`**. `reemplazar_desde` recorre `guia_destino.referencias` (ya cargada) y hace `db.delete()` fila a fila en vez de `query(...).delete(synchronize_session=False)` -- este último deja el identity map desincronizado (`SAWarning` al reinsertar con ids reciclados en SQLite; en PostgreSQL no recicla pero la colección quedaría stale igual).
- **Revalidación server-side del origen**. El `origen_guia_id` del cliente nunca se confía: `_origen_o_404()` recalcula el conjunto {guías importables de hermanas de la AG que el profesor imparte} con el mismo `_guias_hermanas_importables()` del `GET` y comprueba pertenencia -- `404` uniforme ("Guia no encontrada") si no está, mismo mensaje que el resto del hilo de `Guia`. Es la única lectura cross-programa que #184 abre.
- **Orígenes importables** (issue [#740](https://github.com/mmasias/pyCelda/issues/740), 2026-10-09): `Aprobada`, la imparta o no quien importa; `EnRevision`, solo si quien importa también imparte el origen; `Borrador` y `Rechazada` nunca. La relajación de la 404-uniforme mantiene su forma (solo lectura para listar y revalidar) y amplía los estados que cubre. Regla y porqué en [Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/importarBibliografiaDeGuiaHermana/README.md). Importar es una copia: el destino no sigue al origen si después se rechaza, se revoca o cambia.
- **`fecha_estado` derivada**, no columna (`_fecha_estado()`, antes `_fecha_aprobacion()`): última fila de `HistorialCambio` con `campo="estado"` y `valor_nuevo` igual al estado actual de la guía (`Aprobada` o `EnRevision`); si no hay ninguna, fallback `fecha_generacion_pdf` (que `aprobar()`/`escalar_a_aprobada()` fijan) solo para una `Aprobada`, `None` en otro caso.
- **`GuiaResponse` (escalar), no `AbrirGuiaResponse`**: el `POST` devuelve solo los campos propios de la `Guia` (incluido el `estado` ya degradado). La Vista recarga la colección con su propia navegación a `ReferenciasBibliograficas.tsx`.
- **`vinculada` replicada tal cual, sin forzar**. El flujo normal (`c1` de `enviarGuiaARevision()`) garantiza que un origen `Aprobado` por `enviar -> aprobar`, o `EnRevision`, tiene todo vinculado; solo `escalarGuiaAAprobada()` (que bypasea `c1`) produce un origen con candidatas `vinculada=False`. Replicar fila a fila importa específicamente para orígenes escalados.
- **Sin gate de estado en el destino**. `_guia_destino_o_404()` solo comprueba que el `Profesor` imparte la guía, no su `estado`. Importar a una guía `EnRevision` le cambia el contenido sin degradarla (`confirmar_guardado()` solo actúa sobre `Aprobada`) -- idéntico al comportamiento pre-existente de `guardarBorradorGuia()` desde `EnRevision`, que tampoco tiene gate. Un test fija esta conducta (`test_importar_a_guia_en_revision_no_degrada`) para que no cambie en silencio si algún día se introduce un gate general (familia [#219](https://github.com/mmasias/pyCelda/issues/219)).
- **Deuda conocida, no arreglada aquí**: `confirmar_guardado()` no limpia `fecha_generacion_pdf` al degradar `Aprobada -> Borrador`, así que `/pdf` seguiría sirviendo contenido obsoleto -- comportamiento idéntico al pre-existente de `guardarBorradorGuia()` desde `Aprobada`, familia [#219](https://github.com/mmasias/pyCelda/issues/219).

## Referencias

- [`importarBibliografiaDeGuiaHermana()` en Análisis](/RUP/02-analisis/casos-uso/importarBibliografiaDeGuiaHermana/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/importarBibliografiaDeGuiaHermana/README.md).
- [`guardarBorradorGuia()` en Diseño](/RUP/03-diseño/casos-uso/guardarBorradorGuia/README.md) -- `confirmar_guardado()` reutilizado.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) -- hermandad, copia-no-enlace, `activarCursoAcademico()` no implementado.
- Discussion [#58](https://github.com/mmasias/pyCelda/discussions/58) -- sin capa Service, `vinculada: bool`.
