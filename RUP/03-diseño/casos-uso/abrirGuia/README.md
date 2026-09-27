<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > abrirGuia() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirGuia/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirGuia/README.md)|**Diseño**|[Desarrollo](/RUP/04-desarrollo/casos-uso/abrirGuia/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-18
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`abrirGuia()`](/RUP/02-analisis/casos-uso/abrirGuia/README.md): un único endpoint de lectura, sin capa Service -- el Router de FastAPI orquesta directamente contra los repositorios de `Guia`, `PonderacionEvaluacion`, `ReferenciaBibliografica` y `Sesion`, y fusiona vinculadas + pendientes por colección, la misma agregación de lectura que Análisis ya calificó de "no es responsabilidad de `Guia`, es agregación de lectura para la Vista, no una decisión de dominio". `AbrirGuiaResponse` expone además `Guia.sesiones_minimas` (snapshot del umbral de planificación docente, discussion [#206](https://github.com/mmasias/pyCelda/discussions/206)) para el medidor de sesiones que calcula la Vista. Sin ningún método de `Modelo` invocado con lógica propia -- es el primer caso de la rebanada de 9 y el más simple: solo lectura, sin `<<choice>>`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirGuia/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AbrirGuiaView` (React) -- al entrar en la sesión de edición, pide `GET /api/v1/guias/{guia_id}`.
- **API**: `routers/guia.py::abrir_guia(guia_id)` -- función suelta, sin clase controladora (FastAPI es funcional, no orientado a objetos -- ver nota de la discussion [#58](https://github.com/mmasias/pyCelda/discussions/58) y [`RUP/02-analisis/README.md`](/RUP/02-analisis/README.md)); orquesta las llamadas a repositorio y fusiona el resultado.
- **Modelo**: `Guia` (SQLAlchemy) -- sin lógica propia invocada en este caso de uso, solo se serializa lo que ya devuelve `GuiaRepository.obtener()`. Incluye `Guia.contenido` (temario propio, discussion [#191](https://github.com/mmasias/pyCelda/discussions/191)) y `Guia.sesiones_minimas` (umbral de planificación docente, discussion [#206](https://github.com/mmasias/pyCelda/discussions/206)): `AbrirGuiaResponse` los expone en su propio campo, `contenido` distinto de `asignatura_grado.contenido` (referencia estructural). La edición del texto no es de este caso de uso -- la persiste `guardar_borrador_guia()`. `AbrirGuiaResponse` también expone `asignatura_grado` (con `resultados_aprendizaje`/`metodologias_docentes` anidados) y `profesorado`: ambos vienen precargados por las opciones `joinedload`/`selectinload` de `GuiaRepository.obtener()`, no son consultas propias de este caso de uso (issue [#212](https://github.com/mmasias/pyCelda/issues/212)).
- **Repositorio**: `GuiaRepository.obtener(guia_id)` -- con `joinedload(Guia.asignatura_grado).selectinload(resultados_aprendizaje | metodologias_docentes | actividades_formativas)`, `selectinload(Guia.profesorado)` y `selectinload(Guia.sesiones)` como opciones de carga; `GradoRepository.dirige(guia.grado_id, director_grado_id)` -- produce `puede_revisar`, única lectura genuinamente independiente que añade el issue [#212](https://github.com/mmasias/pyCelda/issues/212) (reutiliza la misma pregunta que la guardia de acceso de entrada, aquí como dato de salida); `PonderacionEvaluacionRepository.listar_vinculadas_de(guia)` / `listar_pendientes_de(guia_id)`; `ReferenciaBibliograficaRepository.listar_vinculadas_de(guia)` / `listar_pendientes_de(guia_id)`; `SesionRepository.listar_vinculadas_de(guia)` / `listar_pendientes_de(guia_id)`.

## Decisiones de diseño

- **Fusión vinculadas + pendientes en el Router, no en `Guia`**: Análisis ya decidió que es agregación de lectura para la Vista, sin regla de dominio -- se mantiene la misma asignación de responsabilidad al bajar a código, no se traslada a `Guia` solo porque ahora hay una clase Python concreta donde ponerla.
- **Sin capa Service**: el Router llama a los repositorios directamente, sin salto intermedio -- Router delgado -> Modelo/Repository, decisión ya cerrada en la discussion [#58](https://github.com/mmasias/pyCelda/discussions/58).
- **Lecturas independientes por colección** (`Guia` + 2×`PonderacionEvaluacion` + 2×`ReferenciaBibliografica` + 2×`Sesion` -- las dos de `Sesion` desde el Bloque 2 de la discussion [#206](https://github.com/mmasias/pyCelda/discussions/206)), no una única consulta con joins -- reflejan las colaboraciones de salida de [`colaboracion.puml`](/RUP/02-analisis/casos-uso/abrirGuia/colaboracion.puml) de Análisis; no se introduce una optimización N+1 sin evidencia de que haga falta.
- **`asignatura_grado` y `profesorado` no son lecturas independientes, `puede_revisar` sí** ([issue #212](https://github.com/mmasias/pyCelda/issues/212), corrige una deriva de este artefacto anterior a #206): los dos primeros viajan precargados dentro de la misma llamada a `GuiaRepository.obtener()` (opciones `joinedload`/`selectinload`), así que no suman una consulta nueva al contar colaboraciones; `puede_revisar` sí es una llamada nueva y genuina a `GradoRepository.dirige()`, situada tras `obtener()` y antes de las lecturas de colecciones.
- **`profesorado` de la plantilla en vivo + banner (issue [#254](https://github.com/mmasias/pyCelda/issues/254))**: el campo `profesorado` de `AbrirGuiaResponse` deja de serializar `guia.profesorado` (la copia) y pasa a `guia.asignatura_grado.profesorado` (`[]` si no hay `AsignaturaGrado`). `GuiaRepository.obtener()` gana `selectinload(AsignaturaGrado.profesorado)` y `selectinload(Guia.historial)` -- este último para la propiedad calculada nueva `Guia.comentario_revision_por_profesorado` (`str | None`, patrón `comentario_rechazo`: `estado == "EnRevision"` + última transición `Aprobada -> EnRevision` con `autor_id == 0`), que `AbrirGuiaResponse` expone en un campo propio para el banner del frontend. La copia `guia.profesorado` sigue siendo la que lee el render de `descargarGuiaPDF()`/`previsualizarGuia()`.
- **Los medidores de completitud los calcula la Vista** (Bloque 1 y Bloque 3 de la discussion [#206](https://github.com/mmasias/pyCelda/discussions/206)): total de ponderaciones contra 100% y subtotal por `SistemaEvaluacion` contra su rango; recuento de `Sesion` visibles contra `Guia.sesiones_minimas`. Es agregación de presentación sobre las listas ya fusionadas, no toca backend ni `Guia`.
- **Autenticación fuera de este diagrama**: `profesor_id` llega inyectado por *dependency override* de FastAPI (stub, decisión 3 de la discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)), no se modela como paso propio de la secuencia.
- **`actividades_formativas` sin consulta nueva** (discussion [#227](https://github.com/mmasias/pyCelda/discussions/227), hallazgo de Manuel en producción): `GuiaRepository.obtener()` ya carga `AsignaturaGrado.actividades_formativas` con `joinedload`/`selectinload` desde el PR2 del clúster (lo necesitaba el render, `descargarGuiaPDF()`/`previsualizarGuia()`) -- `AbrirGuiaResponse` solo añade el campo a la serialización, la eager-load ya estaba ahí. Mismo criterio de solo lectura que `resultados_aprendizaje`/`metodologias_docentes`: la edición sigue siendo de [`editarActividadesFormativasAsignaturaGrado()`](/RUP/03-diseño/casos-uso/editarActividadesFormativasAsignaturaGrado/README.md).
- **`fecha_creacion`: columna nueva, nullable, sin backfill**: `Guia.fecha_creacion: datetime | None`, `default=lambda: datetime.now(UTC)` a nivel de modelo -- las altas nuevas la reciben sola, sin tocar `GuiaRepository.crear()` (no pasa el campo explícito, el `default` del `Mapped` se aplica en el `INSERT`). Migración `ALTER TABLE guias ADD COLUMN fecha_creacion DATETIME NULL` (patrón `migrar_sesiones_minimas.py`, PR #211) -- **sin backfill deliberado**: no hay dato histórico real que rellenar (la fecha de alta de las 108 guías existentes no se registró nunca), y rellenar con un valor inventado (p. ej. la fecha del `ALTER`) sería peor que `NULL` -- afirmaría un dato falso en vez de admitir que no se tiene. `AbrirGuiaResponse`/`GuiaResponse` lo exponen como `datetime | None`; el frontend distingue "sin dato" ("Fecha desconocida") de un valor real, en vez del `FUERA_DE_ALCANCE` genérico que usaba antes. **Orden de deploy: el habitual** (`ALTER` antes de `./deploy.sh`, como `migrar_sesiones_minimas.py`) -- a diferencia de `migrar_actividades_formativas.py` del PR1 de #227, este script es raw SQL sin importar código nuevo, no hay riesgo de `ImportError` contra el backend viejo.

## Referencias

- [`abrirGuia()` en Análisis](/RUP/02-analisis/casos-uso/abrirGuia/README.md) -- diagrama de colaboración origen: fusión vinculado+pendiente por colección, sin capa Service.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirGuia/README.md).
- [Discussion #191](https://github.com/mmasias/pyCelda/discussions/191) -- `Guia.contenido` como apartado propio (fase de impartición).
- Discussion [#58](https://github.com/mmasias/pyCelda/discussions/58) -- criterio de arranque de Diseño y las tres decisiones ya cerradas (vinculación, sin endpoint de eliminar, autenticación stub).
- [Issue #212](https://github.com/mmasias/pyCelda/issues/212) -- deriva de este artefacto anterior a #206, cerrada aquí: faltaban `profesorado`, `asignatura_grado` y `puede_revisar` (`GradoRepository.dirige()`) en la secuencia y en los participantes.
- [`abrirAsignaturaGrado()` en Diseño](/RUP/03-diseño/casos-uso/abrirAsignaturaGrado/README.md) -- gestiona `resultados_aprendizaje`/`metodologias_docentes`, que esta pantalla solo muestra de solo lectura.
- [`editarActividadesFormativasAsignaturaGrado()` en Diseño](/RUP/03-diseño/casos-uso/editarActividadesFormativasAsignaturaGrado/README.md) -- gestiona `actividades_formativas`, que esta pantalla solo muestra de solo lectura.
- [Discussion #227](https://github.com/mmasias/pyCelda/discussions/227) -- clúster de `ActividadFormativa`; PR1 (`migrar_actividades_formativas.py`, runbook invertido por dependencias de código nuevo) y PR2 (eager loading de `actividades_formativas` en `GuiaRepository.obtener()`, reutilizado aquí sin cambio).
- [PR #211](https://github.com/mmasias/pyCelda/pull/211) -- `migrar_sesiones_minimas.py`, patrón de migración `ALTER TABLE ... ADD COLUMN` sin ritual extract/reimport, reutilizado para `fecha_creacion`.
