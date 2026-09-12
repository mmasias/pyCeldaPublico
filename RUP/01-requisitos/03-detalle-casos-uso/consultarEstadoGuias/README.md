<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > consultarEstadoGuias()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoGuias/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|`DirectorGrado`|`Admin` (issue [#262](https://github.com/mmasias/pyCelda/issues/262))|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoGuias/wireframe.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoGuias/wireframe-admin.svg)|
|||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorGrado` y `Admin`|
|**Objetivo**|Consultar el listado de `Guia` de un `Grado`, con su estado actual|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

Puerta de entrada al ciclo de revisión del grado: primer caso de uso de L9, abre `GUIAS_DEL_GRADO_ABIERTO`, el listado desde el que se navega a las nueve decisiones/acciones restantes (`abrirGuia()` reutilizado, más `notificarGuiasActualizadas()` como self-loop del propio listado). Mismo patrón que `abrirAsignaturasGrado()`: listado plural sin `<<choice>>`.

**Compartido con `Admin` -- dos propósitos distintos sobre el mismo listado** (`GUIAS_DEL_GRADO_ABIERTO` ya es un estado de `Admin` desde el issue [#6](https://github.com/mmasias/pyCelda/issues/6): reutilizó el tramo `consultarEstadoGuias()` -> `abrirGuia()` para localizar la guía a reabrir por incidencia). El issue [#262](https://github.com/mmasias/pyCelda/issues/262) le da a `Admin` **su propia pantalla y su propio propósito**: monitorear el estado de las guías del grado durante la beta de profesores, no solo localizar una para reabrir. La entrada es `[Estado del curso actual]` en `GradoAdmin` (`/admin/grados/:id/guias`, gemela de `MateriaAdmin`/`AsignaturaGradoAdmin`), independiente de la de `DirectorGrado` (`/grados/:id/guias`). El backend es el mismo endpoint `GET /grados/{grado_id}/guias`, con el gate ampliado a "admin **o** dirige el grado" (patrón de #263/[#220](https://github.com/mmasias/pyCelda/issues/220), 404 uniforme). La fila difiere por actor: el `DirectorGrado` navega a `abrirGuia()` (`[Abrir]`, contexto de revisión); el `Admin` no -- `abrirGuia()` le da 403 -- y en su lugar tiene **`[Previsualizar]`** (`previsualizarGuia()`, `/vista`, cualquier estado -- ya suyo tras #262) y **`[Descargar PDF]`** (`descargarGuiaPDF()`, `/pdf`, ya suyo tras #220; deshabilitado con motivo cuando la guía no tiene `fechaGeneracionPDF`). El botón `[Notificar guías actualizadas]` (self-loop del `DirectorGrado` hacia el `Admin`) no aparece en la pantalla de `Admin` -- no tiene sentido notificarse a sí mismo.

**Forward-compat con `CursoAcademico` (#222)**: la pantalla se llama "curso actual" a propósito. Hoy no hay dimensión de año (una `Guia` por `AsignaturaGrado`), así que se construye sin parámetro; la ruta (`/admin/grados/:gradoId/guias`) y la firma de `listar_guias_del_grado` dejan hueco para un `?curso=` opcional (por defecto el vigente) que llegará con #222, sin construirlo ahora.

**Este mismo contenido se duplica ahora en [`abrirGrado()`](../abrirGrado/README.md)** (retoque de Manuel, 2026-09-05): la portada del grado (`GRADO_ABIERTO`) pasa a mostrar por defecto el listado de `Guia`, variante conservadora que NO fusiona los dos estados/CU -- este caso de uso sigue existiendo tal cual, sin cambio de comportamiento propio.

**Wireframe corregido (2026-09-05)**: al diverger el wireframe de `abrirGrado()` para reproducir este mismo contenido, se detectó que este wireframe llevaba tiempo desactualizado respecto a `ConsultarEstadoGuias.tsx` -- le faltaba el botón `[Notificar guías actualizadas]` (self-loop ya construido y documentado en su propia ficha) y la columna **Última actualización** (`Guia.ultima_actualizacion`/`ultima_actualizacion_rol`, ver [`abrirGuia()`](../abrirGuia/README.md)), y sobraba un botón `[Volver al grado]` que el código real nunca tuvo -- la navegación de vuelta la resuelve `NavGrado` (menú común a toda pantalla de `DirectorGrado`), no un botón propio de esta pantalla. Corregido para no quedar stale justo al lado del wireframe nuevo que reproduce este mismo contenido.

Columna **Estado**: valor de `Guia.estado` (`Borrador`/`EnRevision`/`Aprobada`/`Rechazada`), determina qué decisión ofrece `abrirGuia()` al abrir cada fila -- `[Aprobar]`/`[Rechazar]` si `EnRevision`, `[Escalar a aprobada]` si `Borrador`/`Rechazada`, `[Revocar aprobación]` si `Aprobada` (ver retoque de [`abrirGuia()`](../abrirGuia/README.md) en este mismo lote).

Columna **Última actualización**: `{ultima_actualizacion_rol}, {fecha imprecisa}` -- p. ej. "Profesor, hace dos días" -- `fechaImprecisa()` (`src/fecha.ts`), cuyo único call site es esta lista (`ListaGuiasDelGrado.tsx`, compartida con el gemelo de Admin). Con el issue [#254](https://github.com/mmasias/pyCelda/issues/254), `ultima_actualizacion_rol` gana un tercer valor, **"Administración"**, cuando la última transición de estado es el `Aprobada -> EnRevision` que dispara el `Admin` al cambiar el profesorado (fila de `HistorialCambio` con `autor` centinela).

**Granularidad de la fecha imprecisa (issue [#306](https://github.com/mmasias/pyCelda/issues/306))**: buckets finos cerca, gruesos lejos, con los números en palabra -- `Hace un momento` (< 1 h), `Hoy`, `Ayer`, `Hace {dos..seis} días`, `Hace {una/dos/tres} semanas`, `Hace {un..cuatro} meses`, `Hace mucho tiempo` (≈ 5 meses en adelante). Sustituye a los buckets anteriores (`Esta semana` / `La semana pasada` / `Este mes` / `Hace N meses` / `Hace N años`). El contrato de salida no cambia (mayúscula inicial, el call site hace `.toLowerCase()`).

**Profesorado en vivo (issue [#254](https://github.com/mmasias/pyCelda/issues/254))**: la columna de profesorado del listado deja de leer la copia `Guia -- Profesor` y pasa a leer `AsignaturaGrado -- Profesor` en vivo, igual que [`abrirGuia()`](../abrirGuia/README.md) -- la panorámica del director debe mostrar quién imparte de verdad, no una copia que puede haber quedado por detrás de la plantilla. Sin cambio de comportamiento del caso de uso, solo la fuente del dato.

Una sola fila real en el wireframe (`GII__IYA003`, Programación I) -- única `Guia` confirmada del seed. **Mostrada hipotéticamente en `EnRevision`**: su estado real es `Borrador` (así se ve en el resto del catálogo desde L7); se fuerza aquí de forma ilustrativa, documentada explícitamente, porque el catálogo no tiene todavía una `Guia` real en revisión y el caso de uso pierde sentido si la única fila mostrada nunca ofreciera `[Aprobar]`/`[Rechazar]` -- decisión tomada con el usuario en la discussion [#44](https://github.com/mmasias/pyCelda/discussions/44).

**Badge de color de estado de la `Guia`** (issue [#280](https://github.com/mmasias/pyCelda/issues/280)): la columna `Estado` pasa a mostrar un badge de color -- verde `Aprobada`, ámbar `EnRevision`, rojo `Rechazada`, neutro (gris tenue) `Borrador` -- para que profesor y director lean su cola de un vistazo. 3 señales + reposo: `EnRevision` es la cola de decisión del director y tiene que saltar; `Rechazada` es retrabajo del profesor; `Borrador` no grita nada todavía. El texto se queda siempre (el color es aditivo, accesibilidad), y el badge muestra la etiqueta legible ("En revisión", no el literal del enum). Caja "Leyenda" compacta bajo la tabla. Presentación pura: los 4 estados ya están en [`guia.puml`](/RUP/00-modelo-del-dominio/estados-entidades/guia.puml), el color deriva de `Guia.estado`, sin dato nuevo ni cambio de API. Mapa `estado -> {clase, etiqueta}` en `frontend/src/estadoGuia.ts` (un solo sitio), colores en `index.css`, mismo patrón que la leyenda de `Sesion.tipo` (issue [#266](https://github.com/mmasias/pyCelda/issues/266)) pero con badge en la celda, no fondo de fila. Aplica igual, con la misma pieza, en: [`abrirGuia()`](../abrirGuia/README.md) y las pantallas de acción [`rechazarGuia()`](../rechazarGuia/README.md) / [`revocarAprobacionGuia()`](../revocarAprobacionGuia/README.md) (cabecera, sin caja "Leyenda"); y las **dos** variantes de [`abrirAsignaturasGrado()`](../abrirAsignaturasGrado/README.md) (`TablaMisGuias.tsx` del `Profesor` y `AsignaturasGrado.tsx` del `DirectorGrado`, ambas con caja "Leyenda").

## Referencias

- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) / [de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `GRADO_ABIERTO --> GUIAS_DEL_GRADO_ABIERTO : consultarEstadoGuias()` en ambos
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) / [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catalogado en ambos, sin herencia
- [`previsualizarGuia()`](../previsualizarGuia/README.md) / [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md) -- las dos acciones de fila de la variante `Admin` (issue [#262](https://github.com/mmasias/pyCelda/issues/262))
- [Issue #254](https://github.com/mmasias/pyCelda/issues/254) / [discussion #255](https://github.com/mmasias/pyCelda/discussions/255) -- profesorado del listado en vivo; `ultima_actualizacion_rol` gana "Administración"
- [Diagrama de estados de Guia](/RUP/00-modelo-del-dominio/estados-entidades/guia.puml) -- los cuatro estados mostrados en la columna Estado
- [Discussion #44](https://github.com/mmasias/pyCelda/discussions/44) -- cierre de L9, dato hipotético de `EnRevision` para el wireframe
- [`abrirGrado()`](../abrirGrado/README.md) -- duplica este mismo contenido en `GRADO_ABIERTO`, sin fusionar los estados.
