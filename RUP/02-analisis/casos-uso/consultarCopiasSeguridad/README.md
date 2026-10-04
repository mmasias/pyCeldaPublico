<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > consultarCopiasSeguridad()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/consultarCopiasSeguridad/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/consultarCopiasSeguridad/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`consultarCopiasSeguridad()`](/RUP/01-requisitos/03-detalle-casos-uso/consultarCopiasSeguridad/README.md) (issue [#308](https://github.com/mmasias/pyCelda/issues/308)): un solo paso, sin `<<choice>>`, de solo lectura. Presenta el listado de copias de seguridad de la base de datos que el `Admin` puede diagnosticar -- familia, fecha exacta, tamaño y motivo de cada una --, más reciente primero. Mismo molde que [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) (verbo `consultar`: lectura/monitoreo de un estado que el `Admin` no gestiona, solo observa), con una diferencia que el precedente no cubre: **no hay entidad del modelo del dominio detrás** -- `CopiaSeguridad` no está en [`modeloDominio.puml`](/RUP/00-modelo-del-dominio/modeloDominio.puml); es un fichero plano (`backups_manifest.jsonl`, JSON Lines solo-append) que escribe infraestructura fuera de este repositorio. Por eso el diagrama no tiene `Repository` ni `Guia`/`Programa` que cruzar: la única clase de modelo es el propio manifiesto, que se lee a la defensiva. Ausencia o vacío del manifiesto es un estado válido (lista vacía), no un error; una línea mal formada se descarta sin que el `Admin` lo vea.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/consultarCopiasSeguridad/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `ConsultarCopiasSeguridadView`

**Responsabilidades:**
- presenta el listado de copias de seguridad: `timestamp` (fecha y hora **exactas**, no impreciso -- un `Admin` que diagnostica un incidente necesita saber cuándo se hizo el backup, issue [#306](https://github.com/mmasias/pyCelda/issues/306)), `familia` (etiqueta legible), `archivo` (informativo), `tamanoBytes` (en KB/MB) y `motivo`.
- presenta el estado vacío cuando no hay ninguna copia.
- la vuelta al panel la resuelve el único botón "Volver" de las pantallas de `Admin`, no un menú de navegación propio.

**Colaboraciones:**
- **Entrada:** `:SISTEMA_DISPONIBLE` -- el `Admin` solicita consultar las copias de seguridad (desde [`abrirPanelAdministracion()`](../abrirPanelAdministracion/README.md)).
- **Control:** `CopiaSeguridadController`.
- **Salida:** `:COPIAS_SEGURIDAD_ABIERTO`.

## Clases de controlador

### `CopiaSeguridadController`

**Responsabilidades:**
- lista las copias de seguridad existentes (`listarCopiasSeguridad()`), ordenadas de la más reciente a la más antigua.
- no valida ni muta nada -- caso de uso de solo lectura, sin descarga: no expone rutas del sistema de ficheros más allá del `archivo` informativo del manifiesto.

**Colaboraciones:**
- **Entrada:** `ConsultarCopiasSeguridadView`.
- **Salida:** `ManifiestoCopiasSeguridad`.

## Clases de modelo

### `ManifiestoCopiasSeguridad`

**Responsabilidades:**
- lee el manifiesto (`leerCopias()`) línea a línea, a la defensiva: si el fichero no existe devuelve lista vacía; una línea con JSON inválido o con un campo faltante o de tipo equivocado se salta con un aviso en el log, sin romper la respuesta; el campo opcional de versión de esquema que no sea un entero se trata como ausente, sin descartar la copia.
- cada línea válida es una `CopiaSeguridad` (`timestamp`, `familia` -- `diario`/`puntual`/`pre_restauracion` --, `archivo`, `tamanoBytes`, `motivo`, `esquemaVersion` opcional): objeto de valor leído del fichero, no entidad persistida en la base de datos.
- no es un `Repository`: el origen no es una tabla, es un fichero fuera de la base de datos que escribe infraestructura.

**Colaboraciones:**
- **Entrada:** `CopiaSeguridadController`.

## Fuera de alcance de esta rebanada

**Crear** una copia puntual a demanda y **restaurar** una existente (issues [#629](https://github.com/mmasias/pyCelda/issues/629)/[#632](https://github.com/mmasias/pyCelda/issues/632)/[#634](https://github.com/mmasias/pyCelda/issues/634)) viven hoy en la misma pantalla y el mismo router, pero **no son este caso de uso**: el catálogo de Requisitos no tiene un CU propio para ellas y esta ficha cubre solo el listado de solo lectura. Documentarlas queda para un CU aparte, no se mezcla aquí.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/consultarCopiasSeguridad/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/consultarCopiasSeguridad/wireframes.puml) -- fuente de verdad del listado y de su estado vacío.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SISTEMA_DISPONIBLE --> COPIAS_SEGURIDAD_ABIERTO : consultarCopiasSeguridad()`, `COPIAS_SEGURIDAD_ABIERTO --> SISTEMA_DISPONIBLE : abrirPanelAdministracion()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `CopiaSeguridad` **no** es entidad del dominio (fuera del modelo por capas).
- [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) -- plantilla del verbo `consultar` para lectura/monitoreo sin CRUD.
- [`abrirPanelAdministracion()`](../abrirPanelAdministracion/README.md) -- origen y destino de la navegación.
- [`consultarHistorialCambios()`](../consultarHistorialCambios/README.md) -- caso de uso hermano de auditoría de `Admin`.
