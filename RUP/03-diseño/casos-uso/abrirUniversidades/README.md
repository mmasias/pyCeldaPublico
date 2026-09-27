<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > abrirUniversidades() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirUniversidades/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirUniversidades/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-24
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`abrirUniversidades()`](/RUP/02-analisis/casos-uso/abrirUniversidades/README.md): un solo paso, de solo lectura. Presenta el listado completo de `Universidad` -- primer nivel de la estructura curricular (`Universidad *-d- Facultad`), punto de entrada del `Admin` a toda la gestión de catálogo que cuelga de ella. `UniversidadController` converge en `routers/universidad.py`, módulo nuevo de funciones sueltas.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirUniversidades/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AbrirUniversidadesView` (React) -- pide `GET /api/v1/universidades`; presenta `nombre` por fila.
- **API**: `routers/universidad.py::listar_universidades()` -- función suelta, primera del módulo nuevo.
- **Modelo**: ninguno con lógica propia invocada -- `Universidad` solo porta los datos de cada fila.
- **Repositorio**: `UniversidadRepository.listar()` -- `SELECT` sin filtro: el listado es la totalidad del catálogo de `Universidad`, no una selección propia de quien llama.

## Decisiones de diseño

- **Módulo `routers/universidad.py` nuevo**: primera función de `Universidad` en Diseño; el módulo crecerá con `obtener_universidad()` (de `abrirUniversidad()`), `crear_universidad()` y `editar_universidad()` de los CU hermanos.
- **Listado completo, sin filtro por sesión**: a diferencia de `abrirGrados()` (variante `DirectorGrado`, filtrado por cookie JWT de la discussion [#62](https://github.com/mmasias/pyCelda/discussions/62)), aquí el `Admin` ve todas las filas -- ninguna `Universidad` es "propia" de quien llama.
- **Autorización de `Admin`: `Depends(require_admin)`** (dependencia fijada en el diseño de [`iniciarSesion()`](/RUP/03-diseño/casos-uso/iniciarSesion/README.md), no implementada en este documento) -- toda función de `routers/universidad.py` debe declararla explícitamente en Desarrollo. El historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real, no un detalle menor -- se deja constancia explícita en cada CU de este lote, no solo en uno.
- **Sin capa Service**: Router delgado -> Repository (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).

## Referencias

- [`abrirUniversidades()` en Análisis](/RUP/02-analisis/casos-uso/abrirUniversidades/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirUniversidades/README.md).
- [`abrirUniversidad()` en Diseño](/RUP/03-diseño/casos-uso/abrirUniversidad/README.md) / [`crearUniversidad()` en Diseño](/RUP/03-diseño/casos-uso/crearUniversidad/README.md) -- destinos de navegación del listado.
- [`abrirGrados()` en Diseño](/RUP/03-diseño/casos-uso/abrirGrados/README.md) -- contraste: listado filtrado por sesión (variante `DirectorGrado`).
