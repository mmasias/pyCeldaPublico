<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirPanelAdministracion() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirPanelAdministracion/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirPanelAdministracion/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-24
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`abrirPanelAdministracion()`](/RUP/02-analisis/casos-uso/abrirPanelAdministracion/README.md): primitiva de navegación pura, sin `<<choice>>` ni dato de dominio. A diferencia de todos los demás CU de esta rebanada, no hay nada que bajar a nivel de API/Modelo/Repositorio -- el contenido es un menú fijo de seis enlaces, resuelto enteramente en el cliente (routing de React), sin petición HTTP propia.

Es el destino de la rama `Admin` de [`iniciarSesion()`](/RUP/03-diseño/casos-uso/iniciarSesion/README.md) tras `callback_admin()`.

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirPanelAdministracion/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `PanelAdministracion.tsx` (React, no construida en esta rebanada) -- presenta los accesos (`Universidades`, `Asignaturas`, `Metodologías docentes`, `Actividades formativas`, `Profesores`, `Cursos académicos`, `Copias de seguridad`, `Auditoría`, `Generar guías PDF`) como rutas del propio frontend (`react-router-dom`), sin `fetch` a la API.
- **API / Modelo / Repositorio**: ninguno -- no hay endpoint que diseñar para este CU.

## Decisiones de diseño

- **Sin endpoint de backend**: coherente con Análisis ("sin Controlador ni Modelo") -- el único requisito no funcional es que la ruta del frontend esté protegida (el usuario tiene que haber pasado por `callback_admin()` y portar una cookie de sesión con claim `rol=admin`), pero esa protección la implementa cada endpoint de destino (`Depends(require_admin)`, ver [`iniciarSesion()` en Diseño](/RUP/03-diseño/casos-uso/iniciarSesion/README.md)), no este CU -- que en sí mismo no llama a ningún endpoint.
- **Construcción de `PanelAdministracion.tsx` fuera de esta rebanada**: se fija solo la ruta de llegada (`/panel-administracion`) y que no requiere datos remotos -- mismo criterio que el resto de pantallas todavía no construidas del catálogo.

## Referencias

- [`abrirPanelAdministracion()` en Análisis](/RUP/02-analisis/casos-uso/abrirPanelAdministracion/README.md) -- diagrama de colaboración origen.
- [`iniciarSesion()` en Diseño](/RUP/03-diseño/casos-uso/iniciarSesion/README.md) -- origen de la navegación (rama `Admin`) y de `require_admin`.
- Discussion [#113](https://github.com/mmasias/pyCelda/discussions/113) -- encargo de este Diseño, bloque "Admin bottom-up".
