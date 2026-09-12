<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > descargarGuiaPDF()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/descargarGuiaPDF/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/descargarGuiaPDF/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`, `Profesor` (heredado por `DirectorGrado`)|
|**Objetivo**|Descargar el PDF ya generado de una `Guia`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Compartido entre `Admin` y `Profesor` **sin relación de herencia entre ambos** -- un solo caso de uso, una sola especificación, catalogado de forma independiente en `actoresCasosUsoAdminOperativa.puml` y en `actoresCasosUsoProfesor.puml`, mismo criterio que `abrirGrados()`/`abrirAsignaturaGrado()` reutilizados entre `Admin`/`DirectorGrado`. Self-loop de `GUIA_ABIERTO` en los tres diagramas de contexto (`Profesor`, `DirectorGrado` heredado, `Admin`).

**`<<choice>>` bloqueante en la especificación, pero sin pantalla de bloqueo en el wireframe**: si `fechaGeneracionPDF` está vacía no hay PDF que mostrar, pero el botón `[Descargar PDF]` ya se ofrece condicionalmente en `GUIA_ABIERTO` (ver retoque de [`abrirGuia()`](../abrirGuia/README.md)) -- no aparece cuando el dato está vacío, así que la rama roja nunca se dispara desde esta interfaz. Se mantiene en la especificación como salvaguarda estructural del caso de uso (reutilizable desde otro punto no modelado todavía), no como un flujo real de este wireframe -- decisión cerrada en el punto 2 de la discussion [#44](https://github.com/mmasias/pyCelda/discussions/44).

Wireframe con `GII__IYA003` mostrada hipotéticamente con PDF ya generado (`fechaGeneracionPDF` con valor) -- su estado real (`Borrador`, sin PDF) es justo el caso que el botón condicional excluye; mismo criterio ilustrativo que el resto del lote.

**Contenido del PDF (v1 del render real, discussion [#218](https://github.com/mmasias/pyCelda/discussions/218))**: el binario que este caso de uso sirve deja de ser un placeholder y pasa a ser el render de la plantilla oficial de guía docente de la universidad (`docs/PROPUESTA_PLANTILLA/`), generado en el momento de la descarga a partir de la fila `Guia` y su cascada -- sin almacenar bytes. Seis bloques que el modelo ya rinde: datos generales, contenidos (`Guia.contenido`), resultados de aprendizaje (leídos en vivo de `AsignaturaGrado`), metodologías docentes, sistema de evaluación (convocatoria ordinaria), y bibliografía; más un marcador literal `ACTIVIDADES_FORMATIVAS_AQUI` en su posición, ancla para cuando ese bloque se implemente (discussion [#217](https://github.com/mmasias/pyCelda/discussions/217), enfoque incremental) -- **superado por v2 y v3, ver los dos párrafos siguientes**. El `<<choice>>` de este caso de uso no cambia: el PDF solo se ofrece si `fechaGeneracionPDF` tiene valor, es decir, sobre guías `Aprobada` con `generarGuiasPDF()` ya ejecutado. La vista HTML de la misma guía, disponible en cualquier estado como previsualización, es el caso de uso [`previsualizarGuia()`](../previsualizarGuia/README.md).

**Maquetación al formulario oficial (v2, discussion [#224](https://github.com/mmasias/pyCelda/discussions/224))**: la maquetación del v1 se basó en una guía docente ya rellenada de un formato antiguo (`docs/GII-IYA009.pdf`); v2 la alinea al **formulario oficial en blanco** `docs/PROPUESTA_PLANTILLA/Plantilla-GuiaDocente.pdf` (7 páginas). Cambios de presentación, sin tocar modelo ni flujo: título en texto azul centrado sin banda (solo página 1), secciones numeradas 1-6, celdas de etiqueta en azul saturado con texto blanco, cabecera con logo repetida en cada página, pie "Página X de Y" abajo a la derecha, y -- cuando `estado != Aprobada` -- **marca de agua diagonal "BORRADOR - NO OFICIAL" en todas las páginas** en lugar de la banda de aviso (la banda roja se conserva solo en la vista HTML de [`previsualizarGuia()`](../previsualizarGuia/README.md), que no es paginada). Las seis secciones siempre se renderizan con su esqueleto aunque no haya datos, igual que el propio formulario en blanco: marcador `_REQUISITOS_PREVIOS_AQUI_` (**superado por v4**), tabla de las 10 actividades formativas canónicas con columnas en blanco, convocatoria extraordinaria con el texto oficial fijo y los huecos como "pendiente de concretar", y las 4 subsecciones fijas de bibliografía (básica / complementaria / webs / otras fuentes) con "No aplica" cuando no hay referencias de ese tipo. Cada hueco del backlog de #217 solo se rellena de verdad cuando se construya su bloque.

**Párrafo institucional fijo entre secciones 4 y 5 (issue [#270](https://github.com/mmasias/pyCelda/issues/270))**: cláusula formal idéntica para todas las guías sobre garantía de calidad académica y trazabilidad de la autoría (mínimo del 10 % de las horas lectivas a actividades evaluables con evidencias del proceso de aprendizaje). Boilerplate, no un flag por-guía -- no confundir con el gap #5 de [#217](https://github.com/mmasias/pyCelda/discussions/217).

**Datos reales de actividades formativas (v3, discussion [#227](https://github.com/mmasias/pyCelda/discussions/227))**: la tabla de la sección 4, en blanco desde v2, pasa a leer las horas y el porcentaje de presencialidad reales de `(AsignaturaGrado, ActividadFormativa)` -- el reparto que el `DirectorGrado` teclea en [`editarActividadesFormativasAsignaturaGrado()`](../editarActividadesFormativasAsignaturaGrado/README.md). Las 10 filas se siguen renderizando siempre, en el mismo orden `AF1`..`AF10`, aunque alguna quede a 0 -- ya no dependen de si el reparto está completo. Cierra el último hueco del backlog de #217 sobre esta sección concreta.

**Control de saltos de página y espaciado de cabecera (v5, issue [#268](https://github.com/mmasias/pyCelda/issues/268))**: solo CSS + `<thead>` en dos tablas, sin modelo/flujo. La cabecera corrida deja de pegarse a la primera línea del cuerpo (`padding-bottom` en la caja de margen `@top-left`). Las tablas de sección 4 (actividades formativas) y sección 5 (convocatoria ordinaria) ganan `<thead>` real -> si WeasyPrint parte la tabla entre páginas, la cabecera se repite (`display: table-header-group`). `table { break-inside: avoid }` mantiene enteras las tablas cortas; `h1/h2/h3 { break-after: avoid }` evita títulos huérfanos; los bloques cortos de tamaño fijo (sección 1, subsección de actividades formativas, tabla de convocatoria ordinaria) van en `<div class="bloque">` con `break-inside: avoid`. Las secciones de prosa variable (contenidos, RA, bibliografía) no se envuelven -- solo se protege su título. Sin efecto en la vista HTML no paginada de [`previsualizarGuia()`](../previsualizarGuia/README.md) (`break-*` y `@page` son paged media).

**Requisitos previos como dato real (v4, discussion [#259](https://github.com/mmasias/pyCelda/discussions/259))**: el marcador literal `_REQUISITOS_PREVIOS_AQUI_` de la sección 2 se sustituye por `AsignaturaGrado.requisitosPrevios` (atributo de texto plano nuevo), leído **en vivo** como los RA. Si está vacío o nulo, la sección cae a "No aplica" con el mismo `{% if ... .strip() %}` que ya usa CONTENIDOS. Es el ítem 2 del backlog de #217, adelantado porque la beta de profesores exhibía el token crudo en caja gris. Sin cambio de flujo ni de `<<choice>>`. Lectura en vivo -> editar el campo (`editarAsignaturaGrado()`, `DirectorGrado`) altera guías ya `Aprobada`; el congelado retroactivo se decide en [#219](https://github.com/mmasias/pyCelda/issues/219) junto con los RA.

**El profesorado de la sección 1 lee la copia congelada, no la plantilla en vivo (issue [#254](https://github.com/mmasias/pyCelda/issues/254))**: la fila `DOCENTE` y el correo del formulario oficial renderizan `Guia -- Profesor` (la copia materializada en la última aprobación), **no** `AsignaturaGrado -- Profesor`. Es una divergencia deliberada con las vistas de la app (`abrirGuia()`, listado de guías), que sí leen la plantilla en vivo: el PDF es el registro oficial de lo que el `DirectorGrado` firmó, y no debe cambiar bajo los pies por un cambio de plantilla del `Admin` que aún no ha pasado por re-aprobación. Cuando el director re-aprueba, la copia se sincroniza y el siguiente PDF ya nombra al profesorado nuevo. Sin ramas por estado: `descargarGuiaPDF()` solo sirve guías `Aprobada`, así que la copia siempre está al día con la última firma.

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `GUIA_ABIERTO --> GUIA_ABIERTO : descargarGuiaPDF()`
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- misma transición, sin herencia
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) / [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catalogado en ambos, sin herencia
- [Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) -- `fechaGeneracionPDF`, distinta de `fechaUltimaModificacion`/`fechaCreacion`
- [`generarGuiasPDF()`](../generarGuiasPDF/README.md) -- caso de uso que produce el dato que este consume
- [`previsualizarGuia()`](../previsualizarGuia/README.md) -- vista HTML de la misma guía renderizada, cualquier estado, misma plantilla
- [Issue #254](https://github.com/mmasias/pyCelda/issues/254) / [discussion #255](https://github.com/mmasias/pyCelda/discussions/255) -- el profesorado del PDF lee `Guia -- Profesor` (copia congelada), no la plantilla en vivo
- [Discussion #44](https://github.com/mmasias/pyCelda/discussions/44) -- cierre de L9, punto 2
- [Discussion #217](https://github.com/mmasias/pyCelda/discussions/217) / [#218](https://github.com/mmasias/pyCelda/discussions/218) -- plantilla oficial (el "qué") y motor de render del v1 (el "cómo")
- [Discussion #259](https://github.com/mmasias/pyCelda/discussions/259) -- v4: `AsignaturaGrado.requisitosPrevios` (texto plano en vivo) sustituye el marcador de la sección 2 (ítem 2 de #217)
- [Discussion #224](https://github.com/mmasias/pyCelda/discussions/224) -- v2: maquetación al formulario oficial en blanco (Frente A) y generación de PDF para el usuario (Frente B, caso de uso `generarGuiaPDF()`)
- [Discussion #227](https://github.com/mmasias/pyCelda/discussions/227) -- v3: datos reales de actividades formativas, fuente en [`editarActividadesFormativasAsignaturaGrado()`](../editarActividadesFormativasAsignaturaGrado/README.md)
- [Issue #268](https://github.com/mmasias/pyCelda/issues/268) -- v5: control de saltos de página (`<thead>` repetible, `break-*`) y espaciado cabecera/cuerpo
