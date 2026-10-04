<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirFacultad() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirFacultad/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirFacultad/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-24
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`abrirFacultad()`](/RUP/02-analisis/casos-uso/abrirFacultad/README.md): un solo paso, de solo lectura. Presenta el `nombre` de la `Facultad` y ofrece la navegación a sus `Programa` -- los datos vienen de un único `GET` propio; la pantalla de `Programa` es otro CU (`abrirProgramas()`, cuya variante `Admin` de listado completo de una `Facultad` sigue fuera de alcance del diseño actual), no una segunda consulta de este.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirFacultad/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AbrirFacultadView` (React) -- pide `GET /api/v1/facultades/{facultad_id}`; presenta `nombre` y la navegación (`[Editar]`/`[Ver Programas]`/`[Volver al listado]`).
- **API**: `routers/facultad.py::obtener_facultad(facultad_id)` -- función suelta.
- **Modelo**: ninguno con lógica propia invocada -- `Facultad` solo porta los datos presentados.
- **Repositorio**: `FacultadRepository.obtener(facultad_id)` -- `SELECT` por clave primaria.

## Decisiones de diseño

- **Recurso propio `facultades/{facultad_id}`, no anidado bajo la `Universidad`**: el identificador de `Facultad` es global, mismo criterio que `programas/{programa_id}` ya existente -- la anidación de `abrirFacultades()` era de colección, no de instancia.
- **`404` si el repositorio devuelve `None`**: guardia en la función del Router, mismo mecanismo que el resto de `GET` por identificador del proyecto; no se modela como rama del diagrama porque desde el listado solo se alcanzan identificadores existentes.
- **Reutiliza el endpoint que `editarFacultad()` usará como carga previa**: mismo `GET`, sin duplicar lógica de lectura.
- **Sin capa Service**: Router delgado -> Repository (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).
- **Autorización de `Admin`: `Depends(require_admin)`** (dependencia fijada en el diseño de [`iniciarSesion()`](/RUP/03-diseño/casos-uso/iniciarSesion/README.md), no implementada en este documento) -- toda función de `routers/facultad.py` debe declararla explícitamente en Desarrollo. El historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real, no un detalle menor.

## Referencias

- [`abrirFacultad()` en Análisis](/RUP/02-analisis/casos-uso/abrirFacultad/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirFacultad/README.md).
- [`abrirUniversidad()` en Diseño](/RUP/03-diseño/casos-uso/abrirUniversidad/README.md) -- mismo patrón de `GET` de detalle un nivel arriba.
- [`editarFacultad()` en Diseño](/RUP/03-diseño/casos-uso/editarFacultad/README.md) -- mismo endpoint `GET`, reutilizado como carga del formulario.
