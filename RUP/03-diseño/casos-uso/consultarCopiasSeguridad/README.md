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

Bajada a diseño del caso de análisis [`consultarCopiasSeguridad()`](/RUP/02-analisis/casos-uso/consultarCopiasSeguridad/README.md): `GET /api/v1/copias-seguridad`, listado de solo lectura. **Sin repositorio ni modelo propio y sin acceso a la base de datos**: el origen es el fichero `backups_manifest.jsonl`, que el Router lee a través de un helper de `core/backups.py` (`leer_copias_seguridad()`), no a través de un `Repository`. `CopiaSeguridadController` converge en `routers/copia_seguridad.py::consultar_copias_seguridad()`, función suelta, sin capa Service.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/consultarCopiasSeguridad/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `ConsultarCopiasSeguridadView` (`CopiasSeguridad.tsx`, `/copias-seguridad`) -- pide `GET /api/v1/copias-seguridad`; presenta `timestamp` con fecha y hora exactas, familia con etiqueta legible (`diario` -> "Diario", `puntual` -> "Puntual", `pre_restauracion` -> "Previa a restaurar"; un valor desconocido se muestra tal cual), `archivo`, tamaño en KB/MB y `motivo`; estado vacío si no hay copias. Un `401`/`403` redirige a `/admin/login`.
- **API**: `routers/copia_seguridad.py::consultar_copias_seguridad()` -- función suelta, sin `Session` (no toca la base de datos).
- **Helper de lectura**: `core/backups.py::leer_copias_seguridad()` -- parseo a la defensiva del manifiesto; `ruta_manifiesto_backups()` deriva el directorio del propio `engine` de `app.core.database` (única fuente de verdad del path de `pycelda.db`), sin ruta hardcodeada.
- **Schema**: `CopiaSeguridadResponse` -- `timestamp: datetime`, `familia`, `archivo`, `tamano_bytes`, `motivo` opcional y `esquema_version` opcional.

## Decisiones de diseño

- **Sin `Repository` ni modelo ORM**: el manifiesto es un fichero JSON Lines solo-append que escribe infraestructura (`Claude-pyCelda-Prometeus`) en la raíz del mismo volumen que `pycelda.db`, no una tabla. Un helper de `core/` es la traducción directa de `ManifiestoCopiasSeguridad.leerCopias()` de Análisis; inventar un `CopiaSeguridadRepository` sobre un fichero sería ruido.
- **Parseo a la defensiva, línea a línea**: las líneas las escribe un script bash sin validación. El fichero ausente es lista vacía (`200`, no error); una línea con JSON inválido, un campo obligatorio faltante o de tipo equivocado (`json.JSONDecodeError`, `KeyError`, `TypeError`, `ValidationError`) se salta con un `warning` en el log, nunca rompe la respuesta entera; `esquema_version` es opcional y un valor que no sea entero se trata como ausente en vez de descartar la línea. El `Admin` nunca ve "N líneas corruptas".
- **Orden de salida: `timestamp` descendente** (más reciente primero), ordenado en el helper tras leer todo el fichero.
- **Fecha exacta, no impresión relativa** (issue [#306](https://github.com/mmasias/pyCelda/issues/306)): criterio opuesto al de "Última actualización" de `consultarEstadoGuias()`; mismo dato, formato distinto según para qué se usa.
- **Sin descarga**: ninguna ruta del sistema de ficheros sale del servidor más allá del `archivo` informativo del manifiesto.
- **Sin `alt` de negocio**: ninguna precondición puede rechazar la lectura -- sin `404`, sin `<<choice>>`.
- **El mismo router aloja `POST /copias-seguridad` (crear copia puntual) y `POST /copias-seguridad/restaurar`**: son de los issues [#632](https://github.com/mmasias/pyCelda/issues/632) y [#629](https://github.com/mmasias/pyCelda/issues/629), no de este caso de uso; no se modelan en este diagrama (ver "Fuera de alcance" en Análisis).
- **Sin capa Service**: Router delgado -> helper de `core/` (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).
- **Autorización de `Admin`: `Depends(require_admin)`** -- el listado revela nombres de ficheros y momentos de backup de la infraestructura; el historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real.

## Referencias

- [`consultarCopiasSeguridad()` en Análisis](/RUP/02-analisis/casos-uso/consultarCopiasSeguridad/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/consultarCopiasSeguridad/README.md).
- [`consultarEstadoGuias()` en Diseño](/RUP/03-diseño/casos-uso/consultarEstadoGuias/README.md) -- plantilla del verbo `consultar` (aquí sin base de datos).
- [`consultarHistorialCambios()` en Diseño](/RUP/03-diseño/casos-uso/consultarHistorialCambios/README.md) -- caso de uso hermano de auditoría de `Admin`.
