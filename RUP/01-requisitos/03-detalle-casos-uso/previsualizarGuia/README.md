<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > previsualizarGuia()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/previsualizarGuia/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Borrador (con aviso)|Aprobada (sin aviso)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/previsualizarGuia/wireframe-borrador.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/previsualizarGuia/wireframe-aprobada.svg)|
|||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor` (heredado por `DirectorGrado`) y `Admin`|
|**Objetivo**|Ver la `Guia` renderizada con el formato de la guía docente oficial, en cualquier estado, como previsualización|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Nace del v1 del render real de la guía docente (discussion [#218](https://github.com/mmasias/pyCelda/discussions/218), pregunta P4). [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md) sirve el PDF oficial, y solo cuando `fechaGeneracionPDF` tiene valor (guía `Aprobada` con `generarGuiasPDF()` ya ejecutado). `previsualizarGuia()` sirve la **misma guía renderizada con la misma plantilla**, pero como página HTML de solo lectura y en **cualquier estado** -- un `Profesor` quiere ver cómo va quedando su `Borrador`, un `DirectorGrado` quiere revisar una `EnRevision` antes de aprobar. Si la `Guia` no está `Aprobada`, el sistema presenta un aviso de borrador no oficial.

**`previsualizarGuia`, verbo nuevo del catálogo**: no estaba en la lista de "Nomenclatura" de [`01-actores-casos-uso`](/RUP/01-requisitos/01-actores-casos-uso/README.md), se formaliza ahí como verbo propio -- mismo criterio con el que `selecciona` entró como cuarto verbo de Actor cuando la práctica destapó una distinción real (aquí: render de solo lectura de un artefacto compuesto, sin persistencia, disponible antes de la aprobación -- ni `abrir` una pantalla de gestión, ni `descargar` el artefacto oficial). El sustantivo es `Guia`, entidad del modelo, no "guía docente" -- el matiz "documento institucional renderizado" vive en la prosa, igual que el sufijo `PDF` de `descargarGuiaPDF()`.

**Self-loop de `GUIA_ABIERTO`, sin `<<choice>>`**: disponible en todos los estados de la `Guia` (`Borrador`, `EnRevision`, `Aprobada`, `Rechazada`), así que no hay bifurcación de validación que modelar. El aviso de borrador no oficial es presentación condicional dentro de la rama verde -- el documento se renderiza entero igual, solo se le añade la banda de aviso; no es una rama roja (no hay fallo de precondición). Sin persistencia, sin `HistorialCambio`.

**Actor y autorización**: `Profesor` (autor de la asignatura), `DirectorGrado` (que dirige el grado de la guía) y `Admin` (cualquier guía, para monitorear la beta) -- **404 uniforme**. La discussion [#218](https://github.com/mmasias/pyCelda/discussions/218) P3 fijó el modelo de autorización como "el mismo que `descargarGuiaPDF()` (`Profesor` / `DirectorGrado` / `Admin`, 404 uniforme)"; el v1 dejó a `Admin` **diferido** (§3, opción a) por una razón puramente técnica -- la auth de `Admin` no existía todavía en `routers/guia.py`. La construyó [#238](https://github.com/mmasias/pyCelda/issues/238) para `descargarGuiaPDF()` (cerrando la deriva [#220](https://github.com/mmasias/pyCelda/issues/220)); el issue [#262](https://github.com/mmasias/pyCelda/issues/262) aplica el mismo gate a `previsualizarGuia()` -- gemelo del #220. El portal público de guías para alumnos sigue siendo backlog aparte (D1), no este CU.

Wireframe con `GII__IYA003` (Programación I, Dr. Manuel Masías -- `manuel.masias@uneatlantico.es`), datos del seed: profesorado, contenidos y las cuatro `PonderacionEvaluacion` (Examen Parcial 25% + Actividades y ejercicios 20% + Interés y participación 5% en evaluación continua; Examen Teórico-Práctico 50% en evaluación final) son reales. La pantalla **con aviso** usa su estado real (`EnRevisión`, no `Aprobada`, así que la banda de aviso aplica); la pantalla **Aprobada** la muestra hipotéticamente `Aprobada` para ilustrar la ausencia del aviso -- misma hipótesis puntual que el resto del lote L9. Los bloques de resultados de aprendizaje, metodologías y bibliografía se dejan esquemáticos en el mockup (la maqueta real es trabajo de la plantilla, no del wireframe). La cabecera es logo + "GUÍA DOCENTE 2026-2027", como las guías actuales. El año sale de una **constante de config** (`Settings.curso_academico_vigente`, env var `CURSO_ACADEMICO_VIGENTE`, default `"2026-2027"`) porque el backend del v1 no modela `CursoAcademico` -- issue [#222](https://github.com/mmasias/pyCelda/issues/222) para sustituirla cuando se modele.

**Profesorado: lee la copia congelada, igual que el PDF (issue [#254](https://github.com/mmasias/pyCelda/issues/254))**: la previsualización comparte `_contexto()` con `descargarGuiaPDF()`, así que la sección 1 renderiza `Guia -- Profesor` (la copia de la última aprobación), no la plantilla en vivo -- sin ramas por estado. Para una `Guia` que nunca se aprobó la copia está vacía y la fila `DOCENTE` sale "No aplica": aceptable, esa guía nunca fue oficial y la banda de aviso ya deja claro que es un borrador. Las vistas de gestión (`abrirGuia()`) sí muestran el profesorado en vivo; la previsualización, no, porque enseña "cómo quedará el documento oficial".

**Requisitos previos como dato real (v4, discussion [#259](https://github.com/mmasias/pyCelda/discussions/259))**: la plantilla compartida con [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md) deja de rendir el literal `_REQUISITOS_PREVIOS_AQUI_` en la sección 2 y lee `AsignaturaGrado.requisitosPrevios` (atributo de texto plano nuevo) **en vivo**, igual que los RA -- "No aplica" si está vacío o nulo. Ítem 2 del backlog de #217. La deuda de que editar el campo altere guías `Aprobada` se resuelve en [#219](https://github.com/mmasias/pyCelda/issues/219), común con los RA.

**Párrafo institucional fijo entre secciones 4 y 5 (issue [#270](https://github.com/mmasias/pyCelda/issues/270))**: cláusula formal idéntica para todas las guías (trazabilidad de la autoría, mínimo del 10 % de horas lectivas a actividades evaluables con evidencias). Aparece igual en la vista HTML de este CU y en el PDF de [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md). Boilerplate, no un flag por-guía.

**Control de saltos de página del PDF (v5, issue [#268](https://github.com/mmasias/pyCelda/issues/268))**: los `<thead>` nuevos en las tablas de secciones 4 y 5 de la plantilla compartida y las reglas `break-*` / `@page` son **paged media** -- **no afectan a esta vista HTML** (no paginada). El único cambio que sí llega aquí es estructural (dos `<tr><th>` sueltos pasan a `<thead>`), invisible en el flujo continuo.

**Maquetación al formulario oficial (v2, discussion [#224](https://github.com/mmasias/pyCelda/discussions/224))**: la plantilla compartida con [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md) se alinea al formulario oficial en blanco `docs/PROPUESTA_PLANTILLA/Plantilla-GuiaDocente.pdf`. La vista HTML de este caso de uso **no es paginada**: no lleva cabecera repetida, ni numeración de página, ni la marca de agua diagonal (todo eso es paged media, solo del PDF de `descargarGuiaPDF()`). Cuando la `Guia` no está `Aprobada`, el HTML **conserva la banda de aviso roja** al principio del documento -- es el equivalente no paginado de la marca de agua diagonal del PDF. Que un `Ctrl+P` del navegador sobre esta vista se parezca o no al PDF de WeasyPrint es mejor esfuerzo, no un objetivo de v2 (cerrado con Manuel en #224).

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `GUIA_ABIERTO --> GUIA_ABIERTO : previsualizarGuia()`
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- misma transición, heredada de `Profesor`
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catalogado en el paquete de salida de la guía, junto a `descargarGuiaPDF()`
- [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md) -- misma plantilla, salida PDF oficial (solo `Aprobada` con PDF generado)
- [`generarGuiasPDF()`](../generarGuiasPDF/README.md) -- caso de uso de `Admin` que produce `fechaGeneracionPDF`, sin relación con esta previsualización
- [Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) -- `Guia`, cascada `AsignaturaGrado`/`Materia`/`Grado`/`Facultad`, `ResultadoAprendizaje` leído en vivo; `Guia -- Profesor` (copia congelada, issue #254)
- [Issue #254](https://github.com/mmasias/pyCelda/issues/254) / [discussion #255](https://github.com/mmasias/pyCelda/discussions/255) -- el profesorado de la previsualización lee la copia, no la plantilla en vivo
- [Discussion #217](https://github.com/mmasias/pyCelda/discussions/217) / [#218](https://github.com/mmasias/pyCelda/discussions/218) -- plantilla oficial de guía docente y motor de render del v1
- [Discussion #224](https://github.com/mmasias/pyCelda/discussions/224) -- v2: maquetación al formulario oficial en blanco; divergencia HTML (no paginada, banda roja) / PDF (paginado, marca de agua)
- [Discussion #227](https://github.com/mmasias/pyCelda/discussions/227) -- v3: la tabla de actividades formativas (sección 4, compartida con [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md)) pasa de blanco a datos reales de `(AsignaturaGrado, ActividadFormativa)`
- [Discussion #259](https://github.com/mmasias/pyCelda/discussions/259) -- v4: `AsignaturaGrado.requisitosPrevios` (texto plano en vivo) sustituye el marcador de la sección 2 (ítem 2 de #217)
- [Issue #268](https://github.com/mmasias/pyCelda/issues/268) -- v5: control de saltos de página del PDF (paged media, sin efecto en esta vista salvo `<thead>` estructural)
