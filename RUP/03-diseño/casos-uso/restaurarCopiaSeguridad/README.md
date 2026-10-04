<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > restaurarCopiaSeguridad() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/restaurarCopiaSeguridad/README.md)|[Análisis](/RUP/02-analisis/casos-uso/restaurarCopiaSeguridad/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Bajada a diseño del caso de análisis [`restaurarCopiaSeguridad()`](/RUP/02-analisis/casos-uso/restaurarCopiaSeguridad/README.md): `POST /api/v1/copias-seguridad/restaurar` con cuerpo `{archivo}`. Sin repositorio ni acceso ORM salvo la lectura de `PRAGMA user_version` de la BD viva: el Router valida con `core/backups.py` y encola la sobrescritura como tarea en segundo plano, de modo que la respuesta sale antes de que el proceso muera.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/restaurarCopiaSeguridad/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `CopiasSeguridad.tsx` -- botón Restaurar por fila, panel de confirmación por nombre exacto, aviso de restauración en curso.
- **API**: `routers/copia_seguridad.py::restaurar_copia_seguridad()` -- `Depends(require_admin)`; `logger.warning` con admin y archivo (única auditoría).
- **Helpers**: `core/backups.py` -- `resolver_archivo_backup()`, `preparar_restauracion()`, `crear_backup_puntual()` (para la copia previa) y `ejecutar_restauracion_y_reiniciar()`.
- **Schemas**: `RestaurarCopiaSeguridadRequest` (`archivo`), `RestaurarCopiaSeguridadResponse` (`detalle`).

## Decisiones de diseño

- **Solo nombres del manifiesto**: `resolver_archivo_backup()` rechaza nombres con separadores o ausentes del manifiesto con 404, para que el cuerpo no apunte a rutas arbitrarias.
- **Esquema por fichero real**: `PRAGMA user_version` del fichero de la copia frente al de la BD viva; el `esquema_version` del manifiesto no se usa. Las copias sin marca (0) nunca coinciden.
- **Copia previa antes de tocar nada**: familia `pre_restauracion`, fichero `pyCelda-pre-restauracion-...`, motivo "antes de restaurar X"; solo se crea si todas las validaciones pasan.
- **Escritura atómica**: copia a `<bd>.restaurando` en el mismo directorio, `fsync` y `os.replace`; se borran `-wal`/`-shm` para no aplicar el diario anterior al fichero nuevo.
- **Reinicio por `os._exit(0)`** en `BackgroundTask`, tras enviar la respuesta; Docker (`restart: unless-stopped`) levanta el proceso limpio.
- **Frontend sin reintentos**: tras el 200 el mensaje es fijo (recargar en 30 segundos); los errores de red posteriores no son un fallo.
- **Auditoría solo en log**: no hay fila de dominio que auditar.

## Referencias

- [`restaurarCopiaSeguridad()` en Análisis](/RUP/02-analisis/casos-uso/restaurarCopiaSeguridad/README.md).
- [`comprobarCopiasSeguridad()` en Diseño](/RUP/03-diseño/casos-uso/comprobarCopiasSeguridad/README.md).
