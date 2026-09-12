<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > enviarGuiaARevision()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/enviarGuiaARevision/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Éxito (suma 100%)|Error (rango o suma incorrectos)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/enviarGuiaARevision/wireframe-exito.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/enviarGuiaARevision/wireframe-error.svg)|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/enviarGuiaARevision/wireframe-error-items-sin-guardar.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/enviarGuiaARevision/wireframe-error-planificacion.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor`|
|**Objetivo**|Enviar la `Guia` de una `AsignaturaGrado` a revisión del director de grado, exigiendo, en cascada: que no queden ítems sin guardar (`c1`); que las `PonderacionEvaluacion` cumplan el rango por `SistemaEvaluacion` y sumen exactamente 100% (`c2`); y que la planificación docente tenga al menos `sesiones_minimas` `Sesion` vinculadas (`c3`)|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

**Ítems sin guardar -- alcance** (Bloque 2 de la discussion [#206](https://github.com/mmasias/pyCelda/discussions/206)): la primera comprobación (`c1`, `409`) cubre las tres colecciones de la sesión de edición de la `Guia` -- `PonderacionEvaluacion`, `ReferenciaBibliografica` **y** `Sesion`. Una `Sesion` creada o editada sin pasar por [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) bloquea el envío igual que las otras dos. El backend no contaba las sesiones hasta #206, aunque el RUP de [`crearSesion()`](../crearSesion/README.md)/[`editarSesion()`](../editarSesion/README.md) y el frontend ya asumían el patrón.

**Planificación docente mínima** (`c3`, Bloque 3 de la discussion [#206](https://github.com/mmasias/pyCelda/discussions/206)): tras `c1` y `c2`, la `Guia` sólo pasa a `EnRevision` si sus `Sesion` vinculadas son al menos `Guia.sesiones_minimas` (`422`, mensaje "Planificación docente incompleta: N de M sesiones"). Regla agregada de la misma familia que la suma de ponderaciones = 100% -- la responde `Guia.planificacion_docente_completa()` (Fat Model). El umbral es config de la [`AsignaturaGrado`](../abrirAsignaturaGrado/README.md) editable por Admin (`sesiones_minimas`, por defecto 25, cota 1-100), con snapshot en la `Guia` al nacer -- misma familia que `semestre` y `contenido`. El medidor "N / M sesiones" en [`abrirPlanificacionDocente()`](../abrirPlanificacionDocente/README.md) y en [`abrirGuia()`](../abrirGuia/README.md) hace visible la regla mientras el `Profesor` edita, sin esperar al rechazo.

**Interacción con la importación entre guías hermanas** (issue [#184](https://github.com/mmasias/pyCelda/issues/184)): al importar bibliografía o planificación docente de una guía hermana, las filas copiadas replican el flag `vinculada` **del origen** fila a fila. Un origen `Aprobado` por el flujo normal tiene todas las filas vinculadas (lo garantiza `c1` de arriba), así que sus copias también -- sin efecto sobre este caso de uso. Pero si el origen llegó a `Aprobada` vía [`escalarGuiaAAprobada()`](../escalarGuiaAAprobada/README.md) (que bypasea `c1`) arrastrando candidatas `vinculada=False`, el destino las hereda y **`c1` bloquea su envío** hasta que el `Profesor` las resuelva -- vincularlas vía [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) o borrarlas. Consecuencia real y correcta, no un defecto: viene de la escalación del origen, no de "cualquier guía Aprobada". `c3` sigue midiendo contra `Guia.sesiones_minimas` del destino, que la importación no toca: importar la planificación de una hermana con más sesiones no garantiza cumplir el umbral propio si éste es mayor.

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `GUIA_ABIERTO --> ASIGNATURAS_GRADO_ABIERTO : enviarGuiaARevision()` (éxito) y `GUIA_ABIERTO --> GUIA_ABIERTO : enviarGuiaARevision()` (rechazo, por ítems sin guardar o por validación de ponderaciones -- ambas razones convergen al mismo estado de salida).
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catálogo de casos de uso de `Profesor` sobre `Guia`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Guia *-d- PonderacionEvaluacion`, regla de suma 100% documentada en el README
- [Diagrama de estados de Guia](/RUP/00-modelo-del-dominio/estados-entidades/guia.puml) -- `Borrador -> EnRevision` / `Rechazada -> EnRevision`
- **Corregido tras la fase de Análisis** (rebanada vertical del hilo `Guia`, 2026-08-18): la especificación pasa de un `<<choice>>` a dos encadenados -- primero comprueba que no queden ítems pendientes-sin-vincular (creados o editados en las sub-vistas de `PonderacionEvaluacion`/`ReferenciaBibliografica` sin haber pasado por `guardarBorradorGuia()`), y solo entonces valida rango por `SistemaEvaluacion` y suma total = 100%. Ver [`RUP/02-analisis/casos-uso/enviarGuiaARevision/README.md`](/RUP/02-analisis/casos-uso/enviarGuiaARevision/README.md) para el detalle de ambas comprobaciones.
- **Ampliado en el Bloque 3 de la [discussion #206](https://github.com/mmasias/pyCelda/discussions/206)**: se añade `c3` encadenado tras `c2` (planificación docente < `sesiones_minimas`). Con eso los tres motivos de rechazo del dominio quedan modelados como ramas propias -- se cierra la pregunta abierta que Análisis dejaba señalada sobre si Requisitos necesitaba una tercera rama. Se generan además los dos wireframes que faltaban: el rechazo por ítems sin guardar (`c1`, pendiente desde `3ee9d38`) y el rechazo por planificación docente incompleta (`c3`).
