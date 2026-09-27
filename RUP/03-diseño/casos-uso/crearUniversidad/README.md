<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > crearUniversidad() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearUniversidad/README.md)|[Análisis](/RUP/02-analisis/casos-uso/crearUniversidad/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-24
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`crearUniversidad()`](/RUP/02-analisis/casos-uso/crearUniversidad/README.md): CRUD real e inmediato contra `UniversidadRepository`, sin ninguna capa Service. Un único paso, sin `<<choice>>` -- `Universidad` no tiene ninguna regla de negocio documentada en el modelo de dominio, así que la obligatoriedad de `nombre` se resuelve por esquema de entrada (Pydantic), no por una llamada explícita en la secuencia.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/crearUniversidad/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `CrearUniversidadView` (React) -- formulario mínimo (`nombre`); al confirmar, `POST /api/v1/universidades`.
- **API**: `routers/universidad.py::crear_universidad(datos)` -- función suelta, sin capa Service; delega directo en el repositorio.
- **Modelo**: `Universidad` (SQLAlchemy) -- sin lógica propia invocada: el Repository construye la fila directamente a partir de los campos del formulario, no hay método de dominio que llamar.
- **Repositorio**: `UniversidadRepository.crear(nombre)` -- persistencia real e inmediata, no una mutación de sesión.

## Decisiones de diseño

- **Sin capa Service**: la función del Router llama al repositorio directamente -- decisión ya cerrada en la discussion [#58](https://github.com/mmasias/pyCelda/discussions/58).
- **Validación de obligatoriedad por esquema de entrada**, no por paso explícito de la secuencia: `UniversidadCreate` (Pydantic) exige `nombre` antes de que la función del Router se ejecute -- mismo mecanismo que `ReferenciaBibliograficaCreate` de referencia. `validarDatosObligatorios(nombre)` de Análisis se disuelve en Pydantic, mismo hallazgo ya documentado en el diagrama de clases de Diseño (discussion [#60](https://github.com/mmasias/pyCelda/discussions/60)).
- **`201 Created`** con el objeto creado (incluido su `id`), no `204 No Content` -- la Vista navega de inmediato a `editarUniversidad()` (`<<include>>` ya cerrado en Análisis) y necesita ese `id`.
- **Autorización de `Admin`: `Depends(require_admin)`** (dependencia fijada en el diseño de [`iniciarSesion()`](/RUP/03-diseño/casos-uso/iniciarSesion/README.md), no implementada en este documento) -- toda función de `routers/universidad.py` debe declararla explícitamente en Desarrollo. Especialmente relevante aquí por ser endpoint de escritura: el historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real.

## Referencias

- [`crearUniversidad()` en Análisis](/RUP/02-analisis/casos-uso/crearUniversidad/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearUniversidad/README.md).
- [`crearReferenciaBibliografica()` en Diseño](/RUP/03-diseño/casos-uso/crearReferenciaBibliografica/README.md) -- mismo patrón de creación con `201` + `<<include>>`.
- [`editarUniversidad()` en Diseño](/RUP/03-diseño/casos-uso/editarUniversidad/README.md) -- destino del `<<include>>`.
