# Mockups navegables

> *el mockup se genera desde el diagrama de contexto, no se escribe a mano; el autor puede pasar por alto transiciones que el script no -> (glm-5.2)*

Mockup navegable por actor, derivado automáticamente del diagrama de contexto + wireframes SVG disponibles en el catálogo de detalle. Cada página es un CU (con su wireframe centrado) y una tabla de acciones donde cada botón se mapea a un CU destino. La navegación sigue estrictamente las transiciones del diagrama de contexto del actor.

El artefacto hace de **puente entre requisitos y análisis**: su valor no es solo comunicativo (mockup para validar con el cliente), sino detector. Al forzar el recorrido página por página, expone defectos del catálogo que el diagrama de contexto por sí solo no revela.

## Navegadores por actor

- [Admin](admin/iniciarSesion.md) — 59 páginas (56 con SVG, 3 override manual). Incluye [`abrirPanelAdministracion.md`](admin/abrirPanelAdministracion.md), nueva al planificar Análisis (discussion [#47](https://github.com/mmasias/pyCelda/discussions/47)) -- ver [README de fase](/RUP/01-requisitos/03-detalle-casos-uso/README.md).
- [Director de grado](directorGrado/iniciarSesion.md) — 43 páginas (39 con SVG, 4 override manual).
- [Profesor](profesor/iniciarSesion.md) — 16 páginas (14 con SVG, 2 override manual). Resuelve [issue #42](https://github.com/mmasias/pyCelda/issues/42): `iniciarSesion()` no tiene ficha de detalle propia en el catálogo (el listado de AsignaturaGrado es efecto lateral del login, no un CU independiente), así que su página reutiliza como override manual el wireframe de `abrirAsignaturasGrado` -- CU cuya ficha pertenece a DirectorGrado, con la salvedad de que el botón "Abrir" de ese wireframe se reasigna a `abrirGuia()` (Profesor edita la Guía, no configura la AsignaturaGrado como haría DirectorGrado con `abrirAsignaturaGrado()`). Gana también [`abrirAsignaturasGrado.md`](profesor/abrirAsignaturasGrado.md) (override manual, misma variante filtrada): destino real de `GUIA_ABIERTO --> ASIGNATURAS_GRADO_ABIERTO`, antes `completarGestion()` genérico sin página propia.

## Cómo se genera

[`docs/scripts/generar_mockup_navegable.py`](../scripts/generar_mockup_navegable.py) lee `diagramaContexto<Actor>.puml` y produce las páginas automáticamente.

```bash
python3 docs/scripts/generar_mockup_navegable.py Admin
python3 docs/scripts/generar_mockup_navegable.py Profesor
python3 docs/scripts/generar_mockup_navegable.py DirectorGrado
```

### Verificación tras retocar un wireframe ya mockeado

`CONTEXTUAL_LABELS` (diccionario en `generar_mockup_navegable.py`) transcribe a mano el texto literal de los botones de cada `wireframes.puml` -- es una segunda fuente de verdad, no derivada del propio `.puml`. El riesgo real no es tocar el diccionario (eso ya se corre a mano), es tocar el wireframe de un CU que un lote posterior retoca sin que nadie recuerde actualizar la entrada correspondiente -- ya ha ocurrido cinco veces en el catálogo (`abrirProfesor`, `abrirMateria`, `abrirGrado`, `abrirAsignaturaGrado`, `abrirGuia`, todos retocados desde un lote posterior al que los cerró).

**Regla**: si un lote retoca un `wireframes.puml` de un CU que ya tiene página en el mockup, correr antes de comitear:

```bash
python3 docs/scripts/verificar_contextual_labels.py
```

No elimina la doble fuente de verdad (aparcado hasta que el proyecto entre en fase de Diseño, ver discussion #52) -- solo evita que la deriva quede en silencio hasta la próxima auditoría manual.

Si el CU retocado tiene página propagada al repo hermano público (`github.com/mmasias/pyCeldaPublico`, subconjunto no sensible del proyecto -- expone justo este mockup), regenerar también la página correspondiente allí: copiar el fichero cambiado y reinyectar el breadcrumb propio del público (nunca copia ciega, machacaría esa adaptación), luego auditar enlaces/imágenes internos del público antes de comitear. Commit y push del público van siempre después de verificar el privado, nunca en paralelo.

### Limitación conocida: crearX()/asociarX() muestran la etiqueta de aterrizaje, no su propio botón

`crearX()`/`asociarX()` no tienen estado propio en el diagrama de contexto -- son una arista (transición), no un nodo. Al generar su página, el script no tiene un estado del que leer "qué transiciones salen de aquí", así que reutiliza la tabla del estado de aterrizaje (`cu_to_dst[cu]`) completa -- típicamente el self-loop de `editarX()`. Resultado: la tabla de `crearReferenciaBibliografica.md` (por ejemplo) muestra la fila "Editar" enlazando a `editarReferenciaBibliografica.md`, aunque el único botón dibujado en su propio wireframe sea `[Crear]`. El enlace es correcto -- ahí aterrizas de verdad -- solo el texto de la fila describe el CU invocado (`editarReferenciaBibliografica()`) en vez del botón pulsado.

**Es un error de convención, no de hecho -- y sí es un error, no una imprecisión neutra.** Corrección sobre la redacción original tras una auditoría externa (glm-5.2 vía OpenCode) del repo privado: el propio README de este artefacto declara su contrato como "cada botón se mapea a un CU destino" -- una fila "Editar" bajo un wireframe cuyo único botón dibujado es `[Crear]` viola esa convención declarada, no es solo "distinto criterio de etiquetado". Lo que lo hace aparcable no es que no haya error, es que su **coste de arreglo supera su coste de lectura** mientras el mockup siga siendo evidencia de Requisitos y no UI real: la fuente de verdad (`especificacion.puml`/`README.md` de cada `crearX()`) ya resuelve la ambigüedad sin depender del mockup (la nota de la transición de salida cita el CU real, `editarX()`, junto al wireframe con el botón real), y arreglarlo en el generador exigiría tocar la misma zona que ya arrastra la doble fuente de verdad de `CONTEXTUAL_LABELS` aparcada hasta Diseño (discussion #52) -- remendar solo esto ahora sería una tercera fuente de verdad, o una tanda de overrides manuales que la próxima regeneración machaca. Patrón sistémico (confirmado en `crearFacultad.md`, `crearPonderacionEvaluacion.md`), no aislado. Si el mockup llega a mostrarse a alguien externo antes de fase de Diseño, la prioridad de arreglarlo sube.

### Protección de ediciones manuales

Cualquier página puede marcarse con `<!-- MANUAL OVERRIDE -->` para que el script no la sobrescriba al regenerar. Útil cuando se aplica la convención de "botones visibles sin enlace" u otros ajustes que el script no sabe producir. Mecanismo completo y tipos de celda CdU documentados en [`docs/scripts/README.md`](../scripts/README.md#generar_mockup_navegablepy).

## Convención: botones visibles sin enlace

El script genera la tabla con las transiciones del actor (lo que el actor puede hacer). Cuando el wireframe del CU muestra más botones que las transiciones autorizadas para ese actor, la convención se aplica **a mano** sobre la página generada:

- **Celda CdU vacía**: el actor ve el botón en la interfaz pero no tiene permiso. Indica restricción por rol.
- **Celda CdU con `(pendiente)`**: el actor tiene permiso (la transición está en el diagrama), pero el CU no tiene `wireframe.svg` generado. Indica deuda de catalogación, no de permisos.
- **Celda CdU con `(pendiente wireframe)`**: variante del anterior, para casos donde la distinción conviene dejar explícita en la propia tabla.

La distinción entre celda vacía y celda con `(pendiente)` es informativa: comunica al lector del mockup por qué no hay navegación desde ese botón (permiso vs deuda).

### Decisión: script simple + excepciones a mano (opción C)

Tres opciones se consideraron:

- **A**: aceptar la versión simple del script (sin botones visibles sin enlace). La "ausencia de fila" sustituye a "ausencia de enlace".
- **B**: añadir parser de `wireframes.puml` al script para extraer botones y aplicar la convención completa automáticamente.
- **C**: script simple para el volumen, manejo manual de las páginas con desajuste.

**Elegida: C.** Razón metodológica: aplicar la convención a mano permite percibir el patrón de desajuste. Si el desajuste es puntual (pocas páginas con botones extra), se considera normal — entendible por la variabilidad de un proyecto. Si el desajuste se vuelve patrón (muchas páginas con botones que no corresponden al actor), es síntoma de que el wireframe del catálogo está mezclando acciones de varios actores y conviene separarlos. Esa detección de patrón se pierde si el script lo normaliza automáticamente.

## Hallazgos detectados durante la generación del Admin

El primer uso del artefacto (sobre el actor Admin) reveló:

- **3 CU del diagrama sin detallar**: `cerrarSesion()`, `generarGuiasPDF()`, `reabrirGuiaPorIncidencia()`. Aparecen como `(pendiente)` en las tablas.
- **2 placeholders**: `iniciarSesion.md` (hub del Admin) y `consultarEstadoGuias.md` (entrada a `GUIAS_DEL_GRADO_ABIERTO`). Páginas con marca *Pendiente de detallar* pero con tabla de navegación completa — la navegación se deriva del diagrama aunque el CU no tenga wireframe.
- **17 CU con múltiples wireframes** (`wireframe-X.svg`) mostrados ambos en la misma página con etiqueta legible. La mayoría corresponden a condiciones de bloqueo (`bloqueada`/`confirmacion` para `eliminar/desasignar`, `bloqueada`/`activado` para `activarCursoAcademico`) o de resultado (`error`/`exito`, `formulario`/`error`). El script los detecta automáticamente y los muestra juntos para evitar páginas huérfanas.

Estos hallazgos se revisarán visualmente sobre el artefacto publicado antes de decidir cuáles son deuda real a reportar como issues.

## Detecciones anteriores

- **[Issue #42](https://github.com/mmasias/pyCelda/issues/42)**: al intentar generar la primera página del mockup del Profesor, se detectó que `iniciarSesion()` no tiene ficha de detalle, ni existe un CU `abrirMisAsignaturasGrado()` separado del login. El mockup actuó como detector de un defecto de catálogo que el diagrama de contexto por sí solo no revelaba.

## Divergencia deliberada con el repo privado

Las 116 páginas de este repo llevan un breadcrumb (`Volver: Al inicio / inicio de <Actor>`) justo antes del título, ausente en el repo de trabajo privado -- decisión explícita: el privado lo navega alguien que ya conoce la estructura, el público necesita una salida visible sin depender del botón atrás del navegador. No está en `generar_mockup_navegable.py` (compartido entre ambos repos) para no imponerlo también al privado; se aplica como paso manual tras cada sincronización -- ver historial de commits de este fichero para el script de inyección usado.

## Pendiente

- [x] Profesor: resuelto (ver issue #42 y sección "Detecciones anteriores").
- [x] Director de grado: generado (43 páginas, ver "Navegadores por actor" arriba) -- desfasado desde antes de esta sesión, corregido tras auditoría externa 2026-08-17.
- [ ] Revisar visualmente los multi-wireframes para validar etiquetas y orden.
- [ ] Revisar páginas con desajuste wireframe-vs-diagrama (convención C, aplicada a mano según aparezca).
