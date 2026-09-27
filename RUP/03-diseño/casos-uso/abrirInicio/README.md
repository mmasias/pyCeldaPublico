<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > abrirInicio() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirInicio/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirInicio/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-09-07
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`abrirInicio()`](/RUP/02-analisis/casos-uso/abrirInicio/README.md): primitiva de navegación que compone dos casos de uso ya catalogados. **Sin endpoint de backend propio** -- coherente con Análisis ("sin Controlador ni Modelo"): la pantalla `Inicio.tsx` monta dos secciones y cada una llama al endpoint del caso de uso que incluye.

Es el destino de la rama `Profesor`/`DirectorGrado` de [`iniciarSesion()`](/RUP/03-diseño/casos-uso/iniciarSesion/README.md) (discussion [#274](https://github.com/mmasias/pyCelda/discussions/274)), tras `GET /auth/me`.

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirInicio/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `Inicio.tsx` (React, ruta `/inicio`) -- lee `GET /auth/me`, y según `es_profesor` / `dirige_grados` monta `<TablaMisGuias>` (sección "Mis guías") y/o `<TablaMisGrados>` (sección "Mis grados"). Componentes `components/TablaMisGuias.tsx` y `components/TablaMisGrados.tsx`, extraídos de `MisAsignaturasGrado.tsx` / `Grados.tsx` para reutilizarlos aquí y en las pantallas completas de deep link.
- **API**: ninguna propia. Reutiliza `GET /api/v1/mis-asignaturas-grado` ([`abrirAsignaturasGrado()`](/RUP/03-diseño/casos-uso/abrirAsignaturasGrado/README.md) variante Profesor) y `GET /api/v1/grados` ([`abrirGrados()`](/RUP/03-diseño/casos-uso/abrirGrados/README.md) variante DirectorGrado).
- **Modelo / Repositorio**: ninguno -- vía los casos incluidos.

## Decisiones de diseño

- **Sin endpoint propio, sin estado de servidor**: `abrirInicio()` es routing de cliente más dos peticiones a endpoints ya existentes. El único requisito no funcional es que la ruta esté tras `RequireSession` (cookie de sesión válida) -- que se cumple porque `get_current_rol()` ya no expulsa a una cuenta reconocida (guard de `iniciarSesion()`, #274).
- **Los dos endpoints incluidos pasan a la variante `_opcional` de su dependencia de auth y devuelven `[]` en vez de `403`** (ver [`iniciarSesion()` en Diseño](/RUP/03-diseño/casos-uso/iniciarSesion/README.md) y las fichas de Diseño de `abrirGrados()`/`abrirAsignaturasGrado()`): así una sección cuya capacidad no aplica se presenta vacía, sin necesidad de que el frontend distinga "sin permiso" de "sin datos".
- **Fetch condicional por booleano, no siempre**: `Inicio.tsx` solo pide `/api/v1/grados` si `dirige_grados`, y `/api/v1/mis-asignaturas-grado` si `es_profesor` -- evita una petición que devolvería `[]` seguro. Una cuenta degenerada (ni imparte ni dirige) no hace ninguna de las dos y ve un aviso plano.
- **Rutas `/grados` y `/mis-asignaturas-grado` conservadas** como pantallas completas (deep link), reescritas para montar el mismo componente de tabla + un botón "Volver a inicio".

## Referencias

- [`abrirInicio()` en Análisis](/RUP/02-analisis/casos-uso/abrirInicio/README.md) -- diagrama de colaboración origen.
- [`iniciarSesion()` en Diseño](/RUP/03-diseño/casos-uso/iniciarSesion/README.md) -- origen de la navegación (rama `Profesor`/`DirectorGrado`), guard de rol, payload de `/auth/me`.
- [`abrirGrados()`](/RUP/03-diseño/casos-uso/abrirGrados/README.md) / [`abrirAsignaturasGrado()`](/RUP/03-diseño/casos-uso/abrirAsignaturasGrado/README.md) en Diseño -- endpoints incluidos.
- [`abrirPanelAdministracion()` en Diseño](/RUP/03-diseño/casos-uso/abrirPanelAdministracion/README.md) -- primitiva de navegación análoga para `Admin`.
- Discussion [#274](https://github.com/mmasias/pyCelda/discussions/274) -- cierre de diseño (Opción C).
