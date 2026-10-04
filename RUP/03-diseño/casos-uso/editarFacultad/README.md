<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarFacultad() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarFacultad/README.md)|[Análisis](/RUP/02-analisis/casos-uso/editarFacultad/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-24
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`editarFacultad()`](/RUP/02-analisis/casos-uso/editarFacultad/README.md): CRUD real e inmediato, `PUT /api/v1/facultades/{facultad_id}`, mismo patrón que `editarUniversidad()` un nivel arriba. Sin `alt` de negocio -- solo la validación de forma que Pydantic ya resuelve. `Facultad` gana aquí su método `actualizar(nombre)`. Es también el destino del `<<include>>` de `crearFacultad()`: tras crear, el `Admin` queda editando la `Facultad` recién creada.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/editarFacultad/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EditarFacultadView` (React) -- carga el formulario con `GET /api/v1/facultades/{facultad_id}` (mismo endpoint que `abrirFacultad()`), envía cambios con `PUT`.
- **API**: `routers/facultad.py::editar_facultad(facultad_id, datos)` -- función nueva; sin validación de negocio, solo coordina la actualización.
- **Modelo**: `Facultad.actualizar(nombre)` -- método nuevo, mismo patrón que `Universidad.actualizar(nombre)`.
- **Repositorio**: `FacultadRepository.obtener(facultad_id)` (reutilizado); `.actualizar(facultad)` -- método nuevo.

## Decisiones de diseño

- **Sin `alt` de negocio**: `Facultad` no tiene ninguna regla de validación cruzada en el modelo de dominio -- la única validación es de forma (`nombre` obligatorio), resuelta por `FacultadUpdate` (Pydantic), mismo mecanismo ya documentado en el diagrama de clases de Diseño para `validarDatosObligatorios()`.
- **Sin capa Service**: Router delgado -> Modelo/Repository (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).
- **Reutiliza el `GET` de `abrirFacultad()`**: mismo endpoint de carga, sin duplicar lógica de lectura.
- **`404` si el identificador no existe**, tanto en el `GET` previo como en el `PUT` -- guardia de Router sobre el `None` del repositorio.
- **Autorización de `Admin`: `Depends(require_admin)`** (dependencia fijada en el diseño de [`iniciarSesion()`](/RUP/03-diseño/casos-uso/iniciarSesion/README.md), no implementada en este documento) -- toda función de `routers/facultad.py` debe declararla explícitamente en Desarrollo. Especialmente relevante aquí por ser endpoint de escritura: el historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real.

## Referencias

- [`editarFacultad()` en Análisis](/RUP/02-analisis/casos-uso/editarFacultad/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarFacultad/README.md).
- [`abrirFacultad()` en Diseño](/RUP/03-diseño/casos-uso/abrirFacultad/README.md) -- mismo endpoint `GET`, reutilizado.
- [`crearFacultad()` en Diseño](/RUP/03-diseño/casos-uso/crearFacultad/README.md) -- `<<include>>` de origen.
- [`editarUniversidad()` en Diseño](/RUP/03-diseño/casos-uso/editarUniversidad/README.md) -- mismo patrón de `GET` previo + `PUT` un nivel arriba.
