<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > comprobarCopiasSeguridad() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/comprobarCopiasSeguridad/README.md)|[Análisis](/RUP/02-analisis/casos-uso/comprobarCopiasSeguridad/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Bajada a diseño del caso de análisis [`comprobarCopiasSeguridad()`](/RUP/02-analisis/casos-uso/comprobarCopiasSeguridad/README.md): `POST /api/v1/copias-seguridad/comprobar`, solo lectura. Sin repositorio ni acceso a la base de datos: el Router llama a `core/backups.py::comprobar_salud_copias()`, que recorre el manifiesto y abre cada copia en solo lectura.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/comprobarCopiasSeguridad/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `CopiasSeguridad.tsx` -- botón "Comprobar salud de las copias" (deshabilitado mientras dura), columna "Salud" y resumen de una línea.
- **API**: `routers/copia_seguridad.py::comprobar_copias_seguridad()` -- `Depends(require_admin)`; registra `logger.info` con el recuento.
- **Helper**: `core/backups.py::comprobar_salud_copias()`, que reutiliza `informe_integridad_de_fichero()` (la misma función que `preparar_restauracion()`).
- **Schema**: `SaludCopiaSeguridadResponse` -- `archivo`, `salud` (`ok`/`danada`/`ilegible`/`no_disponible`) y `detalle` opcional.

## Decisiones de diseño

- **`POST` y no `GET`**: es una acción bajo demanda y costosa, no una consulta; aun así no tiene efectos.
- **Misma verdad que restaurar**: una única función de integridad; botón y restauración no pueden discrepar.
- **Distinción dañada/ilegible**: cabecera que no abre como SQLite -> `ilegible`; cabecera legible cuyo informe no es `ok` (o cuya comprobación lanza error de SQLite) -> `danada`, con `detalle` de una sola línea.
- **`no_disponible` sin abrir nada** para nombres con separadores de ruta o ficheros ausentes.
- **Síncrono, sin caché ni tareas en segundo plano**; sin estado ni persistencia.
- **Log**: `logger.info` con admin y recuento; `logger.warning` por copia dañada o ilegible.

## Referencias

- [`comprobarCopiasSeguridad()` en Análisis](/RUP/02-analisis/casos-uso/comprobarCopiasSeguridad/README.md).
- [`consultarCopiasSeguridad()` en Diseño](/RUP/03-diseño/casos-uso/consultarCopiasSeguridad/README.md).
