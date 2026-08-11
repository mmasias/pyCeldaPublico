# Mockups navegables

> *el mockup se genera desde el diagrama de contexto, no se escribe a mano; el autor puede pasar por alto transiciones que el script no -> (glm-5.2)*

Mockup navegable por actor, derivado automáticamente del diagrama de contexto + wireframes SVG disponibles en el catálogo de detalle. Cada página es un CU (con su wireframe centrado) y una tabla de acciones donde cada botón se mapea a un CU destino. La navegación sigue estrictamente las transiciones del diagrama de contexto del actor.

El artefacto hace de **puente entre requisitos y análisis**: su valor no es solo comunicativo (mockup para validar con el cliente), sino detector. Al forzar el recorrido página por página, expone defectos del catálogo que el diagrama de contexto por sí solo no revela.

## Navegadores por actor

- [Admin](admin/iniciarSesion.md) — 58 páginas (56 con SVG, 1 placeholder, 1 override manual).
- [Director de grado](directorGrado/iniciarSesion.md) — 43 páginas (42 con SVG, 1 placeholder, 1 override manual).
- [Profesor](profesor/iniciarSesion.md) — 15 páginas (15 con SVG, 1 override manual). Resuelve [issue #42](https://github.com/mmasias/pyCelda/issues/42): `iniciarSesion()` no tiene ficha de detalle propia en el catálogo (el listado de AsignaturaGrado es efecto lateral del login, no un CU independiente), así que su página reutiliza como override manual el wireframe de `abrirAsignaturasGrado` -- CU cuya ficha pertenece a DirectorGrado, con la salvedad de que el botón "Abrir" de ese wireframe se reasigna a `abrirGuia()` (Profesor edita la Guía, no configura la AsignaturaGrado como haría DirectorGrado con `abrirAsignaturaGrado()`).

## Cómo se genera

[`docs/scripts/generar_mockup_navegable.py`](../scripts/generar_mockup_navegable.py) lee `diagramaContexto<Actor>.puml` y produce las páginas automáticamente.

```bash
python3 docs/scripts/generar_mockup_navegable.py Admin
python3 docs/scripts/generar_mockup_navegable.py Profesor
python3 docs/scripts/generar_mockup_navegable.py DirectorGrado
```

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
- [ ] Director de grado: generar.
- [ ] Revisar visualmente los multi-wireframes para validar etiquetas y orden.
- [ ] Revisar páginas con desajuste wireframe-vs-diagrama (convención C, aplicada a mano según aparezca).
