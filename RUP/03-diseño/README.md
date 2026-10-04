<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# Diseño

Fase que traduce cada caso ya cerrado en [Análisis](/RUP/02-analisis/README.md) a un **diagrama de secuencia**: mismas clases de análisis (Vista/Controlador/Modelo), pero ahora con orden temporal explícito y nombres concretos de tecnología -- FastAPI en el Router, SQLAlchemy en el Modelo. Criterio de arranque, incluidas las tres decisiones ya cerradas antes de escribir el primer `secuencia.puml`, en la discussion [#58](https://github.com/mmasias/pyCelda/discussions/58).

**Estado actual: 121 carpetas con ficha de Diseño (recuento verificado contra las carpetas en el issue [#662](https://github.com/mmasias/pyCelda/issues/662) y tras la auditoría [#704](https://github.com/mmasias/pyCelda/issues/704); el detalle histórico que sigue conserva la cifra de #658: recuento verificado en el issue [#658](https://github.com/mmasias/pyCelda/issues/658); la cifra histórica era 98 de los 109 casos de uso)** (incluidas las tres primitivas de navegación con ficha, `iniciarSesion()`/`abrirPanelAdministracion()`/`abrirInicio()`) -- ver [casos de uso](casos-uso/README.md). Mismo alcance que [Análisis](/RUP/02-analisis/README.md), trabajado por pipeline vertical por CU: (1) los 22 que cierran el ciclo de vida de `Guia` (L7-L9, más `previsualizarGuia()` de la discussion [#218](https://github.com/mmasias/pyCelda/discussions/218)); (2) los 21 del catálogo de `DirectorPrograma` (L2-L6), más los 3 del clúster de `ActividadFormativa` (discussion [#227](https://github.com/mmasias/pyCelda/discussions/227)); (3) el catálogo de `Admin` (L0-L1) con `iniciarSesion()`; (4) `PlanificacionDocente`/`Sesion` (L10); (5) importación y arranque de la planificación docente entre `AsignaturaPrograma` hermanas (L8/L10, familia del issue [#184](https://github.com/mmasias/pyCelda/issues/184)) -- `importarBibliografiaDeGuiaHermana()` y `importarPlanificacionDocenteDeGuiaHermana()` (router propio `importar_guia_hermana.py`), `generarPlanificacionDocenteGenerica()` (en `routers/sesion.py`, sin origen ni lectura cross-programa). Del primer lote, solo `eliminarPonderacionEvaluacion()`/`eliminarReferenciaBibliografica()` no tienen endpoint de backend -- decisión 2 de la discussion [#58](https://github.com/mmasias/pyCelda/discussions/58), son mutación de la lista de trabajo del cliente; `abrirPonderacionEvaluacion()` es el único caso que no añade endpoint propio: reutiliza tal cual el de `editarPonderacionEvaluacion()`. El lote (2) arrancó los módulos `routers/programa.py`, `routers/materia.py`, `routers/asignatura_programa.py` y `routers/resultado_aprendizaje.py`; los grupos (3) y (4) añadieron el resto hasta los 15 routers actuales, incluidos `routers/auth.py` y `routers/sesion.py`.

## Formato

Una carpeta por caso de uso en `casos-uso/<cu>/`, con dos ficheros:

- **`secuencia.puml`** -- diagrama de secuencia (no de colaboración: aquí sí importa el orden temporal de los mensajes).
- **`README.md`** -- ficha con bloque fijo: Información del artefacto (Proyecto/Fase RUP/Disciplina/Versión/Fecha/Autor), Propósito, el diagrama embebido, Participantes (una línea por capa: Vista/API/Modelo/Repositorio) y Decisiones de diseño.

## Sin capa Service

pyCelda usa **Router delgado -> Modelo con el método -> Repository solo persiste**, sin capa Service intermedia -- decisión ya especificada en los 9 diagramas de colaboración de Análisis (`Guia.puedeEnviarseARevision()`, `Guia.sincronizarPonderaciones()` viven en el Modelo) y confirmada en la discussion [#58](https://github.com/mmasias/pyCelda/discussions/58) contra el código real de pySigHor. Cada `secuencia.puml` baja directamente Vista -> Router -> Modelo -> Repository -> BD, sin el salto a un `*Service` intermedio.

Las clases `*Controller` del diagrama de clases de Análisis son B/C/E, agnósticas de tecnología -- no se traducen a una clase Controller real: cada una converge en un módulo `routers/<entidad>.py` con una función suelta por método, no una clase (FastAPI es funcional, no orientado a objetos).

## Configuración del proyecto

Estructura de directorios del backend (`backend/app/{models,schemas,repositories,routers,core}`, sin `services/`), stack (Python + FastAPI + SQLAlchemy + SQLite) y mapeo artefacto-código -- ver [`configuracion-proyecto.md`](configuracion-proyecto.md).

## Modelo de datos (vista relacional)

El diagrama de clases de arriba es la vista **OO** (clases con métodos, Fat Model). La vista **relacional** del almacén de datos -- las 23 tablas, incluidas las 6 de unión invisibles en la vista OO, con sus FK físicas/lógicas, tipos y dominios -- vive en [`modelo-datos/`](modelo-datos/README.md): `DER.puml` (entidad-relación, notación de pySigHor) y `diccionario-datos.md`. Criterio en la discussion [#196](https://github.com/mmasias/pyCelda/discussions/196).

**Regla de mantenimiento**: un PR que toca `backend/app/models/` regenera el DER y el diccionario (`python -m app.scripts.generar_modelo_datos`) y revisa la capa de intención de diseño a mano -- misma obligación que actualizar el [README del modelo de dominio](/RUP/00-modelo-del-dominio/README.md). `generar_modelo_datos.py --check` es la comprobación.

## Diagrama de clases (recapitulación consolidada)

Vista estática de diseño: unión incremental de las clases Vista/API/Modelo/Repositorio que aparecen, repartidas, en los 89 `secuencia.puml` -- un peldaño más abajo que el [diagrama de clases de Análisis](/RUP/02-analisis/diagrama-clases-analisis.puml) (#59), con nombres concretos de Python (`snake_case`) en vez de firmas agnósticas de tecnología. No introduce ningún método, atributo o relación que no esté ya en algún `secuencia.puml` o en la sección Participantes de su README -- ver discussion [#60](https://github.com/mmasias/pyCelda/discussions/60).

<div align=center>

|![](/images/RUP/03-diseño/diagrama-clases-diseño.svg)|
|-|
|<div align=right><sup>Código fuente: [diagrama-clases-diseño.puml](diagrama-clases-diseño.puml)</sup></div>|

</div>

<div align=center>

|Capa|Color|
|-|-|
|Vista|`#629EF9`|
|API (módulo de funciones, no clase)|`#b5bd68`|
|Modelo|`#F2AC4E`|
|Repositorio|`#D98E73`|
|Estado de entrada / colaboraciones de salida|`#CDEBA5`|

</div>

**Confirmación de lo que #59/#60 anticipaban, ahora con las 22 colaboraciones del hilo `Guia`** (las 21 originales de L7-L9 más `previsualizarGuia()`, [#218](https://github.com/mmasias/pyCelda/discussions/218)): las 22 clases de Vista son idénticas a las de Análisis (React, sin cambio de capa); `GuiaController` (12 métodos en Análisis) converge sin colisión en `routers/guia.py` (12 funciones: `abrir_guia`, `guardar_borrador_guia`, `enviar_guia_a_revision`, `aprobar_guia`, `rechazar_guia`, `escalar_guia_a_aprobada`, `revocar_aprobacion_guia`, `editar_semestre_guia`, `listar_guias_del_programa`, `notificar_guias_actualizadas`, `descargar_guia_pdf`, `previsualizar_guia`) -- las dos últimas delegan el render en el módulo `render/guia_docente.py` (Jinja2 + WeasyPrint para el PDF, Jinja2 solo para la vista HTML; una plantilla, dos salidas -- discussion [#218](https://github.com/mmasias/pyCelda/discussions/218)); `PonderacionEvaluacionController` (5 CU en Análisis) converge en `routers/ponderacion_evaluacion.py` con **seis funciones**, no cinco: las cinco del CU (`cargarSistemasEvaluacion` → `listar_sistemas_evaluacion`, `crearPonderacionEvaluacion`, `cargarPonderacionEvaluacion` → `obtener_ponderacion_evaluacion`, `guardarCambios` → `editar_ponderacion_evaluacion`, `listarPonderacionesEvaluacion`) más `listar_sistemas_evaluacion_de_guia`, que no es un CU propio -- es la segunda lectura de [`abrirPonderacionesEvaluacion()`](casos-uso/abrirPonderacionesEvaluacion/README.md) (catálogo de `SistemaEvaluacion` de la materia para el medidor de rango), ausente de este diagrama consolidado hasta el issue [#212](https://github.com/mmasias/pyCelda/issues/212); `ReferenciaBibliograficaController` (5 CU en Análisis) converge en `routers/referencia_bibliografica.py`, con **cuatro funciones**, no cinco -- `eliminarReferenciaBibliografica()` sigue sin endpoint (decisión 2 de #58).

**Repositorio, capa nueva que Análisis no separaba**: `GuiaRepository`/`PonderacionEvaluacionRepository`/`ReferenciaBibliograficaRepository` ya estaban en el Modelo de Análisis (mismo paquete, mismo color); aquí se separan en su propio paquete porque el README de cada `secuencia.puml` ya los documentaba como línea propia (Vista/API/Modelo/Repositorio). `MateriaRepository`/`SistemaEvaluacionRepository` son adiciones de Diseño, ausentes en Análisis -- ver `crearPonderacionEvaluacion()`/`editarPonderacionEvaluacion()` para la justificación (repositorios mínimos de solo lectura, necesarios para materializar en memoria clases que Análisis referencia sin repositorio propio). `ReferenciaBibliograficaRepository.obtener()`/`.actualizar()` son adiciones de este lote de 12, introducidas por `abrirReferenciaBibliografica()`/`editarReferenciaBibliografica()` -- cierran la asimetría con `PonderacionEvaluacionRepository`, que ya tenía ambos métodos desde los 9 originales.

**Hallazgo de la discussion #60, corregido**: `validarDatosObligatorios()` (`PonderacionEvaluacionController`/`ReferenciaBibliograficaController` en Análisis) se disolvía en el diagrama sin ninguna nota que explicara por qué, a diferencia de `confirmarEliminacion()` (que sí la tenía). Añadidas ambas notas: la validación de obligatoriedad se traslada a `schemas/` (Pydantic) -- `PonderacionEvaluacionCreate`/`Update` y `ReferenciaBibliograficaCreate`/`Update` exigen los campos antes de que la función del router se ejecute, mismo mecanismo ya citado en las Decisiones de diseño de [`crearReferenciaBibliografica()`](casos-uso/crearReferenciaBibliografica/README.md). No es un hueco -- es validación de forma resuelta por el framework, fuera de la capa que este diagrama cubre.

**`ReferenciaBibliografica.actualizar()` cierra la asimetría con `PonderacionEvaluacion.actualizar()`**: ambos hallazgos que la discussion #59 señalaba como "alcance, no hueco" en Análisis quedan resueltos de verdad al bajar a Diseño -- `editarReferenciaBibliografica()` (este lote) tiene su propio `secuencia.puml`, y el `<<include>>` de `crearReferenciaBibliografica()` apunta ahora a una vista real (`EditarReferenciaBibliograficaView`), no a un placeholder.

**Lote DirectorPrograma L2-L6, confirmación con los 21 nuevos**: las 21 clases de Vista vuelven a ser idénticas a las de Análisis; los cuatro Controladores nuevos convergen sin colisión en módulos de funciones -- `ResultadoAprendizajeController` (5 CU) en `routers/resultado_aprendizaje.py` (6 funciones: el CRUD más el chequeo `esta_asignado()` de la eliminación bloqueante), `MateriaController` (8 CU) en `routers/materia.py` (12 funciones), `AsignaturaProgramaController` (7 CU) en `routers/asignatura_programa.py` (12 funciones, entre ellas `obtener_para_editar()`/`editar_asignatura_programa()` con el `<<choice>>` de `semestreDefault`) y `ProgramaController` (2 CU) en `routers/programa.py` (2 funciones). `abrirAsignaturasPrograma()` y `editarAsignaturaPrograma()` reutilizan métodos del hilo `Guia` sin duplicarlos: `GuiaRepository.listar_del_programa(programa_id)` (ya existente) y `GuiaRepository.existe_alguna_de(asignatura_programa_id)` (método nuevo del repositorio existente). Las asociaciones simples (`Materia`-`ResultadoAprendizaje`, `AsignaturaPrograma`-`MetodologiaDocente`/`ResultadoAprendizaje`) se persisten desde el repositorio del agregado -- solo `MetodologiaMateria`, con `descripcion_propia` propia, tiene repositorio propio.

## Pendiente

- **`RUP/04-desarrollo/`**: fase separada, enlaza a ficheros reales del código (no los duplica) más el contrato de endpoint y un campo Estado (`Completado`/`Pendiente`). Todos los CU escalados a Diseño tienen ya implementación real en Desarrollo; solo quedan 3 CU de `Admin` sin código real: `eliminarMateria()`, `generarGuiasPDF()`, `reabrirGuiaPorIncidencia()`.
- **`notificarGuiasActualizadas()` sin mecanismo de envío decidido**: el `secuencia.puml` documenta el disparo como nota interna del Router, sin comprometerse con SMTP/cola/lo que sea -- esa decisión se toma en Desarrollo, si y cuando se construya de verdad.
- **`descargarGuiaPDF()`/`editarSemestreGuia()` dependen de la generación real de PDF**: ninguno de los dos modela cómo se genera o almacena el archivo -- esa pieza pertenece a `generarGuiasPDF()` (`Admin`), caso de uso todavía no escalado a ninguna disciplina.
