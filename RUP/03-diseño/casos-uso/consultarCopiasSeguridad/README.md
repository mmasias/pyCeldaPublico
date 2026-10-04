<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > consultarCopiasSeguridad() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/consultarCopiasSeguridad/README.md)|[Análisis](/RUP/02-analisis/casos-uso/consultarCopiasSeguridad/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-10-03
- **Autor**: Claude Sonnet 5.5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`consultarCopiasSeguridad()`](/RUP/02-analisis/casos-uso/consultarCopiasSeguridad/README.md): `GET /api/v1/copias-seguridad`, listado sin efectos. **Sin repositorio ni modelo propio y sin acceso a la base de datos**: el origen es el fichero `backups_manifest.jsonl`, que el Router lee a través de un helper de `core/backups.py` (`leer_copias_seguridad()`), no a través de un `Repository`. `CopiaSeguridadController` converge en `routers/copia_seguridad.py::consultar_copias_seguridad()`, función suelta, sin capa Service.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/consultarCopiasSeguridad/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `ConsultarCopiasSeguridadView` (`CopiasSeguridad.tsx`, `/copias-seguridad`) -- pide `GET /api/v1/copias-seguridad` y `GET /api/v1/version`; presenta `timestamp` con fecha y hora exactas, familia con etiqueta legible (`diario` -> "Diario", `puntual` -> "Puntual", `pre_restauracion` -> "Previa a restaurar"; un valor desconocido se muestra tal cual), `archivo`, tamaño en KB/MB, `esquema_version` y `motivo`; la columna Salud vacía hasta comprobar; botón "Restaurar" por fila, deshabilitado con el motivo como tooltip si la copia no es restaurable; casilla "Mostrar todos (incluye no restaurables)" (por defecto solo restaurables) con contador "Mostrando X de Y copias"; estado vacío si no hay copias. Un `401`/`403` redirige a `/admin/login`.
- **API**: `routers/copia_seguridad.py::consultar_copias_seguridad()` -- función suelta, sin `Session` (no toca la base de datos).
- **Helper de lectura**: `core/backups.py::leer_copias_seguridad()` -- parseo a la defensiva del manifiesto, y `_estado_fichero_copia()` para `disponible` y `esquema_version`; `ruta_manifiesto_backups()` deriva el directorio del propio `engine` de `app.core.database` (única fuente de verdad del path de `pycelda.db`), sin ruta hardcodeada.
- **Schema**: `CopiaSeguridadResponse` -- `timestamp: datetime`, `familia`, `archivo`, `tamano_bytes`, `motivo` opcional, `esquema_version` opcional y `disponible` (bool, por defecto `true`).

## Decisiones de diseño

- **Sin `Repository` ni modelo ORM**: el manifiesto es un fichero JSON Lines solo-append que escribe infraestructura (`Claude-pyCelda-Prometeus`) en la raíz del mismo volumen que `pycelda.db`, no una tabla. Un helper de `core/` es la traducción directa de `ManifiestoCopiasSeguridad.leerCopias()` de Análisis; inventar un `CopiaSeguridadRepository` sobre un fichero sería ruido.
- **Parseo a la defensiva, línea a línea**: las líneas las escribe un script bash sin validación. El fichero ausente es lista vacía (`200`, no error); una línea con JSON inválido, un campo obligatorio faltante o de tipo equivocado (`json.JSONDecodeError`, `KeyError`, `TypeError`, `ValidationError`) se salta con un `warning` en el log, nunca rompe la respuesta entera; `esquema_version` es opcional y un valor que no sea entero se trata como ausente en vez de descartar la línea. El `Admin` nunca ve "N líneas corruptas".
- **`disponible` y `esquema_version` salen del fichero real, no del manifiesto**: `_estado_fichero_copia(archivo)` abre la copia del volumen en solo lectura (`PRAGMA user_version`), la misma fuente que usa la restauración; el `esquema_version` del manifiesto se ignora porque lo escribe un script externo y puede desincronizarse. Nombre con separadores o fichero ausente -> `disponible=false`, `esquema_version=null`, sin abrir nada; fichero que no abre como SQLite -> `disponible=true`, `esquema_version=null`; nunca excepción.
- **Decisión: restaurabilidad = `disponible` && `esquema_version` == versión viva, decidida en el frontend**: la versión viva la da `GET /api/v1/version`; si no se puede consultar, ninguna copia es restaurable. El backend no marca "restaurable" en el listado: la reverifica al restaurar (`409` si el esquema no coincide, `404` si no existe), de modo que el frontend solo gobierna la presentación (botón deshabilitado, motivo en tooltip, filtro).
- **Orden de salida: `timestamp` descendente** (más reciente primero), ordenado en el helper tras leer todo el fichero.
- **Fecha exacta, no impresión relativa** (issue [#306](https://github.com/mmasias/pyCelda/issues/306)): criterio opuesto al de "Última actualización" de `consultarEstadoGuias()`; mismo dato, formato distinto según para qué se usa.
- **Filtro de restaurables solo en frontend**: no altera la respuesta del listado; el backend siempre devuelve todas las copias.
- **Sin descarga**: ninguna ruta del sistema de ficheros sale del servidor más allá del `archivo` informativo del manifiesto.
- **Sin `alt` de negocio**: ninguna precondición puede rechazar la lectura -- sin `404`, sin `<<choice>>`.
- **El mismo router aloja las acciones de la pantalla** (`POST /copias-seguridad`, `/copias-seguridad/comprobar`, `/copias-seguridad/restaurar`): son los casos de uso [`crearCopiaSeguridad()`](/RUP/03-diseño/casos-uso/crearCopiaSeguridad/README.md), [`comprobarCopiasSeguridad()`](/RUP/03-diseño/casos-uso/comprobarCopiasSeguridad/README.md) y [`restaurarCopiaSeguridad()`](/RUP/03-diseño/casos-uso/restaurarCopiaSeguridad/README.md); no se modelan en este diagrama.
- **Sin capa Service**: Router delgado -> helper de `core/` (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).
- **Autorización de `Admin`: `Depends(require_admin)`** -- el listado revela nombres de ficheros y momentos de backup de la infraestructura; el historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real.

## Referencias

- [`consultarCopiasSeguridad()` en Análisis](/RUP/02-analisis/casos-uso/consultarCopiasSeguridad/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/consultarCopiasSeguridad/README.md).
- [`consultarEstadoGuias()` en Diseño](/RUP/03-diseño/casos-uso/consultarEstadoGuias/README.md) -- plantilla del verbo `consultar` (aquí sin base de datos).
- [`consultarHistorialCambios()` en Diseño](/RUP/03-diseño/casos-uso/consultarHistorialCambios/README.md) -- caso de uso hermano de auditoría de `Admin`.
