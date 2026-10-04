<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/consultarCopiasSeguridad/README.md) / [Diseño](/RUP/03-diseño/casos-uso/consultarCopiasSeguridad/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > consultarCopiasSeguridad()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/consultarCopiasSeguridad/README.md)|[Diseño](/RUP/03-diseño/casos-uso/consultarCopiasSeguridad/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/consultarCopiasSeguridad/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Con datos|Vacío|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/consultarCopiasSeguridad/wireframe.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/consultarCopiasSeguridad/wireframe-vacia.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Consultar qué copias de seguridad de la BD existen, con su familia, fecha, tamaño, versión de esquema y motivo, y cuáles se pueden restaurar -- diagnóstico sin descarga, con acceso a crear una copia, comprobar su salud y restaurar|
|**Tipo**|Primario, de apoyo (soporte a la operación, no a la enseñanza)|
|**Nivel**|Objetivo de usuario|

</div>

**Caso de uso nuevo** (issue [#308](https://github.com/mmasias/pyCelda/issues/308), origen: el `Admin` no tenía forma de ver qué copias de seguridad de la BD existen). Nace del manifiesto `backups_manifest.jsonl` que `Claude-pyCelda-Prometeus` escribe en la raíz del mismo volumen donde vive `pycelda.db` -- JSON Lines, solo-append, una línea por backup (`timestamp`, `familia`, `archivo`, `tamano_bytes`, `motivo`), unificando las familias de backup (diarios automatizados, puntuales pre-deploy/a demanda y previas a una restauración) que hasta ahora el `Admin` no podía ver desde ningún sitio. El listado actual muestra, por copia, Familia, Fecha, Tamaño, Esquema, Motivo, Salud y Restaurar; la familia `pre_restauracion` se rotula "Previa a restaurar".

**Verbo `consultar`, no `abrirX()`**: `CopiaSeguridad` no es una entidad de [`modeloDominio.puml`](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- es un fichero plano fuera de la BD, sin alta/edición/baja, sin `<<choice>>` de validación posible. `abrirX()`/`abrirXs()` está reservado a catálogos reales del dominio con CRUD gestionado por `Admin` (`Universidad`, `Profesor`, `SistemaEvaluacion`...). El precedente correcto es [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md): lectura de solo-monitoreo sobre un estado que el `Admin` no gestiona, solo observa.

**Alcance: listar y dar acceso a las acciones, no descargar.** Sin endpoint de descarga de ficheros ni rutas de filesystem expuestas más allá del `archivo` del manifiesto. Desde esta misma pantalla el `Admin` dispone de tres acciones, cada una con su propio caso de uso: "Hacer copia de seguridad ahora" ([`crearCopiaSeguridad()`](../crearCopiaSeguridad/README.md)), "Comprobar salud de las copias" ([`comprobarCopiasSeguridad()`](../comprobarCopiasSeguridad/README.md), que rellena la columna Salud) y "Restaurar" en cada fila ([`restaurarCopiaSeguridad()`](../restaurarCopiaSeguridad/README.md)). La columna Salud está vacía hasta que se pulsa comprobar.

**Restaurabilidad por fichero real.** Una copia es restaurable si su fichero está disponible en el volumen y su versión de esquema coincide con la de la aplicación en ejecución. Ambos datos salen del propio fichero de la copia, no del manifiesto. Cuando no lo es, su botón "Restaurar" aparece deshabilitado y su ayuda emergente da el motivo: no disponible en el volumen, versión de esquema ilegible o esquema incompatible con la actual. Por defecto el listado muestra solo las restaurables; la casilla "Mostrar todos (incluye no restaurables)" muestra todas, y un contador indica "Mostrando X de Y copias". Si hay copias pero ninguna restaurable, la pantalla indica "No hay copias restaurables todavía. Activa el toggle para ver el historial completo."

**Sin `<<choice>>`, self-loop conceptual de `SISTEMA_DISPONIBLE`**: a diferencia de `enviarGuiaARevision()` o incluso de `crearPonderacionEvaluacion()`, no hay ninguna precondición que pueda rechazar esta lectura. El manifiesto ausente (instalación nueva, o backfill de Prometeus todavía no desplegado) o vacío es un **estado válido del listado** -- lista vacía, `200`, con su propio wireframe de estado vacío -- no un error. Una línea del manifiesto mal formada (JSON inválido, campo faltante -- lo escribe un script bash sin validación) se salta a nivel de backend, invisible para este caso de uso: el `Admin` nunca ve "N líneas corruptas", ve el listado de lo que sí se pudo leer.

**Fecha exacta, no `fechaImprecisa()`** (issue [#306](https://github.com/mmasias/pyCelda/issues/306)): un `Admin` diagnosticando un incidente necesita saber exactamente cuándo se hizo un backup, no "hace mucho tiempo" -- criterio opuesto al de la columna "Última actualización" de [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md), donde la imprecisión es la elección correcta para la planificación del profesor. Mismo dato (`timestamp`), formato distinto a propósito según para qué se usa.

Alcanzable desde [`abrirPanelAdministracion()`](../abrirPanelAdministracion/README.md) (el panel de `Admin`), como el resto de áreas de catálogo -- pero sin gemelo de listado en el sentido `abrirXs()`/`abrirX()`: no hay detalle al que navegar desde una fila, es un listado plano de un solo nivel.

## Notas de diseño y trazabilidad

- Fecha y hora exactas, sin `fechaImprecisa()` (issue [#306](https://github.com/mmasias/pyCelda/issues/306)): la precisión importa en un diagnóstico de incidente. El tamaño se muestra legible (KB/MB), no en bytes crudos. El motivo y el esquema muestran "--" si no hay valor. La columna Salud está vacía hasta comprobar.

- Alcance actual: la pantalla creció con la creación a demanda (#629/#632), la restauración (#629, #631), la versión de esquema por copia (#630), el filtro de restaurables (#634), la restaurabilidad por fichero real (#677), el impedimento de restaurar copias dañadas (#681) y la comprobación de salud (#683). Cada acción tiene su ficha; esta cubre el listado y la regla de restaurabilidad. Se retira el "solo lectura, sin acciones" y el "diario/puntual" de la versión inicial (#308).

- Restaurabilidad (#677, #633, #635, #679): `disponible` y `esquema_version` se leen del fichero real de la copia en el volumen; el `esquema_version` del manifiesto se ignora. El frontend decide la restaurabilidad comparando con la versión de esquema de la aplicación en ejecución; el backend la reverifica al restaurar y rechaza con conflicto si no coincide. Si no se puede consultar la versión actual, ninguna copia se considera restaurable.

- Filtro (#634): es solo de presentación, no borra ni altera nada; la comprobación de salud (#683) cubre también las copias ocultas por el filtro y la pantalla avisa de las dañadas o ilegibles que quedan ocultas.

- Un manifiesto ausente o vacío es un estado válido, no un error (por ejemplo, Prometeus todavía no hizo el backfill); la pantalla muestra "No hay copias de seguridad registradas todavía."

- Modelado: lectura pura, sin precondición que pueda rechazarla (issue [#308](https://github.com/mmasias/pyCelda/issues/308)): el manifiesto ausente o vacío es un estado válido (lista vacía), no un error -- sin `<<choice>>`, mismo criterio que `consultarEstadoGuias()`.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SISTEMA_DISPONIBLE --> COPIAS_SEGURIDAD_ABIERTO : consultarCopiasSeguridad()`, vuelta con `abrirPanelAdministracion()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- package "Copias de seguridad", `Admin -- consultarCopiasSeguridad`
- [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) -- precedente del verbo `consultar` para lectura/monitoreo sin CRUD
- [`abrirPanelAdministracion()`](../abrirPanelAdministracion/README.md) -- origen y destino de la navegación
- Issue [#308](https://github.com/mmasias/pyCelda/issues/308) -- origen del caso de uso, esquema del manifiesto
- [`crearCopiaSeguridad()`](../crearCopiaSeguridad/README.md), [`comprobarCopiasSeguridad()`](../comprobarCopiasSeguridad/README.md) y [`restaurarCopiaSeguridad()`](../restaurarCopiaSeguridad/README.md) -- acciones disponibles desde esta pantalla
- Issue [#306](https://github.com/mmasias/pyCelda/issues/306) -- por qué esta pantalla no reutiliza `fechaImprecisa()`
