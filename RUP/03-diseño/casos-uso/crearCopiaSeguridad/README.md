<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearCopiaSeguridad() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearCopiaSeguridad/README.md)|[Análisis](/RUP/02-analisis/casos-uso/crearCopiaSeguridad/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Bajada a diseño del caso de análisis [`crearCopiaSeguridad()`](/RUP/02-analisis/casos-uso/crearCopiaSeguridad/README.md): `POST /api/v1/copias-seguridad`, con cuerpo `{motivo}` opcional y respuesta `201`. El Router llama a `core/backups.py::crear_backup_puntual()`, que copia la base de datos viva con la API de backup de `sqlite3` y anota el manifiesto. Sin repositorio.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/crearCopiaSeguridad/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `CopiasSeguridad.tsx` -- botón "📦 Hacer copia de seguridad ahora", panel con campo de motivo opcional y botones Crear/Cancelar; tras crear, recarga el listado.
- **API**: `routers/copia_seguridad.py::crear_copia_seguridad()` -- `Depends(require_admin)`; registra `logger.info` con admin y archivo.
- **Helper**: `core/backups.py::crear_backup_puntual()` -- copia, escribe y anota; usa `obtener_version_esquema()`.
- **Schema**: `CrearCopiaSeguridadRequest` (`motivo` opcional) y `CopiaSeguridadResponse`.

## Decisiones de diseño

- **API de backup de `sqlite3`**: copia consistente aunque la base de datos viva esté en uso; solo la lee, nunca la modifica.
- **Familia `puntual` con `esquema_version` real** (`PRAGMA user_version` de la base de datos viva): la copia nace restaurable.
- **Nombre**: `pyCelda-puntual-YYYYMMDD-HHMMSS.db` (UTC); si ya existe, sufijo `-2`, `-3`... para que dos copias seguidas no se pisen.
- **Sin validación del motivo**: texto libre; el frontend envía `null` si está vacío tras `trim()`.
- **Función compartida**: `preparar_restauracion()` reutiliza `crear_backup_puntual()` con otra familia, prefijo y origen para su copia previa.
- **Errores**: 401/403 sin rol Admin (el frontend redirige a `/admin/login`); cualquier otro fallo se muestra en el panel.
- **Log**: `logger.info("Backup puntual: admin=%s archivo=%s")`.

## Referencias

- [`crearCopiaSeguridad()` en Análisis](/RUP/02-analisis/casos-uso/crearCopiaSeguridad/README.md).
- [`consultarCopiasSeguridad()` en Diseño](/RUP/03-diseño/casos-uso/consultarCopiasSeguridad/README.md).
