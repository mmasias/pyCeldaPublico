<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirPlanificacionDocente()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirPlanificacionDocente/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Con sesiones|Vacía (arranque)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirPlanificacionDocente/wireframe.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirPlanificacionDocente/wireframe-vacia.svg)|
|||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor`|
|**Objetivo**|Ver el listado de `Sesion` de la `PlanificacionDocente` de la Guía|
|**Tipo**|Secundario|
|**Nivel**|Subfunción|

</div>

Catálogo inline en un único estado de contexto (`PLANIFICACION_DOCENTE_ABIERTO`), a diferencia del patrón lista/detalle de [`abrirPonderacionesEvaluacion()`](../abrirPonderacionesEvaluacion/README.md)/[`abrirReferenciasBibliograficas()`](../abrirReferenciasBibliograficas/README.md): `Sesion{numero, tipo, descripcion}` es lo bastante simple para que crear/editar/eliminar se resuelvan como formularios propios sin necesitar un estado de detalle separado -- decisión cerrada en discussion [#140](https://github.com/mmasias/pyCelda/discussions/140).

Una única entrada, desde `GUIA_ABIERTO` -- a diferencia de `abrirPonderacionesEvaluacion()`, no hay retorno desde un estado de detalle propio (no existe), así que la única forma de volver a este listado tras crear/editar/eliminar una `Sesion` es el self-loop de esos mismos casos de uso sobre `PLANIFICACION_DOCENTE_ABIERTO`. La salida hacia `GUIA_ABIERTO` reutiliza [`abrirGuia()`](../abrirGuia/README.md), ya cerrado -- sin caso de uso nuevo de "volver" (decisión 8 de discussion #140).

**Medidor de planificación docente mínima** (discussion [#206](https://github.com/mmasias/pyCelda/discussions/206), regla `c3` de [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md)): bajo el listado, **"Planificación docente: N sesiones (mínimo M)"**, con **"(faltan M-N)"** y resaltado en rojo cuando `N < M`, donde `M = Guia.sesiones_minimas`. El "mínimo M" es permanente, no condicional -- que la planificación esté completa (p. ej. 30/25) no debe leerse como si sobraran sesiones. Hace visible mientras el `Profesor` edita la condición de envío que hoy solo se descubre al recibir el rechazo. Se cuentan las `Sesion` visibles (las que se enviarán en `ids_sesiones_final` y quedarán vinculadas), mismo criterio que el medidor de ponderaciones de [`abrirPonderacionesEvaluacion()`](../abrirPonderacionesEvaluacion/README.md). El mismo medidor aparece en la sección "Planificación docente" de [`abrirGuia()`](../abrirGuia/README.md). El texto anterior ("N / M sesiones -- mínimo para enviar a revisión") se retira: la coletilla "para enviar a revisión" confunde al `DirectorGrado` que aprueba (deuda anotada en [#258](https://github.com/mmasias/pyCelda/issues/258), no se resuelve aquí). Es presentación: no cambia el flujo ni la especificación, solo el `wireframe`.

**Leyenda de colores de fila por `Sesion.tipo`** (issue [#266](https://github.com/mmasias/pyCelda/issues/266), reproduce la leyenda del SigHor original): fondo pastel de la fila según el tipo -- celeste `CLASE_TEORICA`, verde `CLASE_PRACTICA`/`CLASE_LABORATORIO`, amarillo `CLASE_TEORICO_PRACTICA`, sin fondo `EVALUACION_CONTINUA`/`EVALUACION_PARCIAL`. Caja "Leyenda" compacta encima de la tabla. Presentación pura: el color deriva de `tipo` (que ya viaja en la respuesta), sin dato nuevo ni cambio de API. Mapa `tipo -> clase` en `frontend/src/sesionTipo.ts` (un solo sitio), colores en `index.css`. Aplica igual en la sección "Planificación docente" de [`abrirGuia()`](../abrirGuia/README.md).

**Retocado al construir el issue [#184](https://github.com/mmasias/pyCelda/issues/184)**: el wireframe gana el botón `[Importar de asignatura hermana]` junto a `[+ Crear Sesión]` -- dispara [`importarPlanificacionDocenteDeGuiaHermana()`](../importarPlanificacionDocenteDeGuiaHermana/README.md), self-loop sobre `PLANIFICACION_DOCENTE_ABIERTO` (reemplaza al completo la planificación docente con la de una `Guia` `Aprobada` de una `AsignaturaGrado` hermana, renumerando `1..N`). Botón condicional: ausente si ninguna hermana tiene guía aprobada. `Guia.sesiones_minimas` del destino no se toca al importar -- el medidor de arriba sigue contando contra el umbral propio.

**Retocado al construir `generarPlanificacionDocenteGenerica()` (familia del issue [#184](https://github.com/mmasias/pyCelda/issues/184))**: la variante de estado vacío del wireframe gana el botón `[Crear N sesiones genéricas]` (N = `Guia.sesiones_minimas`) junto a `[+ Crear Sesión]` -- dispara [`generarPlanificacionDocenteGenerica()`](../generarPlanificacionDocenteGenerica/README.md), self-loop sobre `PLANIFICACION_DOCENTE_ABIERTO` (crea de golpe N `Sesion` planas `CLASE_TEORICA` vinculadas, numeradas `1..N`, para arrancar). **Solo en el estado vacío**: en cuanto hay una `Sesion`, el botón desaparece (el caso de uso responde `409` si se fuerza). Sin tocar la especificación de `abrirPlanificacionDocente()`.

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `GUIA_ABIERTO --> PLANIFICACION_DOCENTE_ABIERTO : abrirPlanificacionDocente()`
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catálogo de casos de uso de `Profesor` sobre `PlanificacionDocente`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Guia *-- PlanificacionDocente`, `PlanificacionDocente *-- Sesion`
- [Discussion #140](https://github.com/mmasias/pyCelda/discussions/140) -- cierre de las 8 decisiones de diseño de la Planificación docente
- [`importarPlanificacionDocenteDeGuiaHermana()`](../importarPlanificacionDocenteDeGuiaHermana/README.md) -- caso de uso disparado desde esta pantalla (issue [#184](https://github.com/mmasias/pyCelda/issues/184))
