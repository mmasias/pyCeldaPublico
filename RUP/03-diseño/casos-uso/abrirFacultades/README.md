<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > abrirFacultades() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirFacultades/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirFacultades/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-24
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`abrirFacultades()`](/RUP/02-analisis/casos-uso/abrirFacultades/README.md): un solo paso, de solo lectura. Presenta el listado de `Facultad` de una `Universidad` concreta -- `Facultad` no es catálogo plano sino composición real (`Universidad *-d- Facultad`), así que el filtro por `universidad_id` vive en la URL y en el `WHERE`, no en la sesión ni en filtrado post-consulta. `FacultadController` converge en `routers/facultad.py`, módulo nuevo de funciones sueltas.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirFacultades/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AbrirFacultadesView` (React) -- pide `GET /api/v1/universidades/{universidad_id}/facultades`; presenta `nombre` por fila, con `[Abrir]`/`[Eliminar]` y `[+ Crear Facultad]`.
- **API**: `routers/facultad.py::listar_facultades(universidad_id)` -- función suelta, primera del módulo nuevo; la colección cuelga de la `Universidad` en la URL.
- **Modelo**: ninguno con lógica propia invocada -- `Facultad` solo porta los datos de cada fila.
- **Repositorio**: `FacultadRepository.listar_de_la_universidad(universidad_id)` -- `SELECT` con `WHERE universidad_id = :universidad_id`.

## Decisiones de diseño

- **Ruta anidada bajo la `Universidad`**: `GET /api/v1/universidades/{universidad_id}/facultades`, no un plano `/api/v1/facultades?universidad_id=...` -- la composición del modelo de dominio (`Universidad *-d- Facultad`) se expresa en la URL, mismo criterio que `guias/{guia_id}/referencias-bibliograficas` ya aplica.
- **`listar_de_la_universidad()` es traducción directa de `listarDeLaUniversidad()` de Análisis** (camelCase -> snake_case): el filtro vive en el `WHERE`, sin filtrado post-consulta.
- **Módulo `routers/facultad.py` nuevo**: crecerá con `obtener_facultad()` (de `abrirFacultad()`), `crear_facultad()`, `editar_facultad()`, `tiene_grados_asociados()` y `eliminar_facultad()` de los CU hermanos.
- **Sin capa Service**: Router delgado -> Repository (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).
- **Autorización de `Admin`: `Depends(require_admin)`** (dependencia fijada en el diseño de [`iniciarSesion()`](/RUP/03-diseño/casos-uso/iniciarSesion/README.md), no implementada en este documento) -- toda función de `routers/facultad.py` debe declararla explícitamente en Desarrollo. El historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real, no un detalle menor.

## Referencias

- [`abrirFacultades()` en Análisis](/RUP/02-analisis/casos-uso/abrirFacultades/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirFacultades/README.md).
- [`abrirFacultad()` en Diseño](/RUP/03-diseño/casos-uso/abrirFacultad/README.md) / [`crearFacultad()` en Diseño](/RUP/03-diseño/casos-uso/crearFacultad/README.md) / [`eliminarFacultad()` en Diseño](/RUP/03-diseño/casos-uso/eliminarFacultad/README.md) -- casos de uso alcanzados desde el listado.
- [`abrirUniversidad()` en Diseño](/RUP/03-diseño/casos-uso/abrirUniversidad/README.md) -- pantalla desde la que se navega hasta aquí.
