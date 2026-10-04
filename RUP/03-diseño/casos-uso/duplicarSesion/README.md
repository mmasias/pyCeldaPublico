<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > duplicarSesion() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/duplicarSesion/README.md)|[Análisis](/RUP/02-analisis/casos-uso/duplicarSesion/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-10-03
- **Autor**: Claude Sonnet 5.5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`duplicarSesion()`](/RUP/02-analisis/casos-uso/duplicarSesion/README.md): CRUD real e inmediato contra `SesionRepository`, sin capa Service y **sin `<<choice>>`**. Un solo paso -- duplicar -- sobre una `Sesion` ya persistida: sin formulario, sin carga previa de selector. La copia se inserta con `numero` = origen + 1 y las posteriores se renumeran +1; la respuesta devuelve el envelope completo ya renumerado, para que el frontend no re-derive la numeración. `PlanificacionDocenteController` converge en `routers/sesion.py`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/duplicarSesion/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `DuplicarSesionView` (React) -- botón `📑 Duplicar` por fila persistida de `PlanificacionDocente`; envía `POST /api/v1/sesiones/{sesion_id}/duplicar` sin cuerpo y reemplaza el listado con la respuesta.
- **API**: `routers/sesion.py::duplicar_sesion(sesion_id)` -- función suelta, sin capa Service; usa `autorizar_escritura_guia()` (`routers/guia.py`) para resolver el rol de quien escribe.
- **Modelo**: `Sesion` -- creada por el repositorio, sin método propio invocado (el desplazamiento es una actualización masiva de `numero`, no una regla del objeto); `HistorialCambio.registrar()` -- fila de auditoría.
- **Repositorio**: `SesionRepository.obtener(sesion_id)` / `duplicar(sesion_id)` -- copia `tipo`+`descripcion`, `numero` = origen + 1, renumera las posteriores en una única transacción.

## Decisiones de diseño

- **Sin capa Service**: el Router llama al repositorio directamente -- decisión ya cerrada en la discussion [#58](https://github.com/mmasias/pyCelda/discussions/58).
- **Persistencia inmediata, a diferencia del resto de la familia de `Sesion`**: el `POST` escribe en el acto y registra su propio `HistorialCambio` (issue [#420](https://github.com/mmasias/pyCelda/issues/420)); la copia nace con `vinculada = false` (default del modelo), igual que una `Sesion` recién creada.
- **Renumeración en el Repository, en una sola transacción**: `SesionRepository.duplicar()` incrementa el `numero` de las posteriores y añade la copia antes de hacer `commit`; `Sesion.numero` no tiene índice único, así que el orden de las actualizaciones intermedias es indiferente y un fallo a mitad no deja la numeración a medias.
- **Respuesta con el envelope completo** (`AbrirPlanificacionDocenteResponse`), no solo la copia -- mismo patrón que `generarPlanificacionDocenteGenerica()`: las demás filas cambian de `numero`.
- **`HistorialCambio` se añade en el `POST`, no en el repositorio**: `duplicar_sesion()` cuenta las sesiones de la `Guia` antes y después (`valor_anterior = "n sesiones"`, `valor_nuevo = "n+1 sesiones"`) y construye la fila con `HistorialCambio.registrar(...)`, que persiste con el `commit` final del endpoint.
- **Autorización por la `Guia` de la `Sesion`**: `404 Sesion no encontrada` uniforme si la `Sesion` no existe o si ni el `Profesor` imparte la `AsignaturaPrograma` ni el `DirectorPrograma` dirige el `Programa`. Si escribe el `DirectorPrograma` (corrección excepcional, issue [#612](https://github.com/mmasias/pyCelda/issues/612)), `aplicar_transicion_por_correccion_del_director()` mueve la `Guia` antes de escribir (Aprobada -> Borrador, EnRevision -> Rechazada).
- **Sin `<<include>>` ni navegación**: se queda en el listado de `abrirPlanificacionDocente()`.

## Referencias

- [`duplicarSesion()` en Análisis](/RUP/02-analisis/casos-uso/duplicarSesion/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/duplicarSesion/README.md).
- [`crearSesion()` en Diseño](/RUP/03-diseño/casos-uso/crearSesion/README.md) -- plantilla estructural (misma entidad); contraste: allí `siguiente_numero()` y sin renumeración, 201 con la `Sesion` nueva.
- [`abrirPlanificacionDocente()` en Diseño](/RUP/03-diseño/casos-uso/abrirPlanificacionDocente/README.md) -- el listado desde el que se invoca y al que se vuelve.
- Discussion [#58](https://github.com/mmasias/pyCelda/discussions/58) -- criterio de arranque de Diseño, sin capa Service.
- Issue [#364](https://github.com/mmasias/pyCelda/issues/364) -- duplicar una sesión.
