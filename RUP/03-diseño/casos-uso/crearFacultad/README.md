<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > crearFacultad() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearFacultad/README.md)|[Análisis](/RUP/02-analisis/casos-uso/crearFacultad/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-24
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`crearFacultad()`](/RUP/02-analisis/casos-uso/crearFacultad/README.md): CRUD real e inmediato contra `FacultadRepository`, sin capa Service. La fila se crea con `universidad_id` desde el principio -- pertenece a su `Universidad` desde el momento de crearse (`Universidad *-d- Facultad`, composición, no catálogo plano). Un único paso, sin `<<choice>>`: la obligatoriedad de `nombre` se resuelve por esquema de entrada (Pydantic), no por una llamada explícita en la secuencia.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/crearFacultad/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `CrearFacultadView` (React) -- formulario mínimo (`nombre`); al confirmar, `POST /api/v1/universidades/{universidad_id}/facultades`.
- **API**: `routers/facultad.py::crear_facultad(universidad_id, datos)` -- función suelta, sin capa Service; delega directo en el repositorio.
- **Modelo**: `Facultad` (SQLAlchemy) -- sin lógica propia invocada: el Repository construye la fila directamente a partir del `universidad_id` de la URL y los campos del formulario, no hay método de dominio que llamar.
- **Repositorio**: `FacultadRepository.crear(universidad_id, nombre)` -- persistencia real e inmediata; la fila nace dentro de la `Universidad` de la URL.

## Decisiones de diseño

- **Esquema nuevo: `facultades` + `Grado.facultad_id`**. La tabla `facultades` es enteramente nueva (`Base.metadata.create_all()` la crea sin tocar tablas existentes -- SQLite solo crea tablas ausentes, nunca altera una ya existente). Pero `Facultad *-- Grado` (modelo de dominio) exige que `Grado` gane una columna `facultad_id` (FK a `facultades.id`) que hoy no tiene (`backend/app/models/grado.py` confirmado sin ella) -- y `Base.metadata.create_all()` **no** añade columnas a una tabla ya existente en SQLite, mismo tipo de drift de esquema ya vivido y documentado al construir `seed_grado.py`. Materialización real, cuando este CU llegue a Desarrollo: (1) exportar/backup los `Grado` reales existentes; (2) recrear el esquema completo con el modelo ya actualizado (`facultad_id` nullable inicialmente, para no romper filas existentes sin Facultad asignada todavía); (3) reimportar los datos y, en un paso aparte, asignar `facultad_id` real a cada `Grado` migrado (mapeo manual -- hoy no hay `Facultad` real en la base de datos con la que emparejar automáticamente); (4) evaluar más adelante si `facultad_id` pasa a `NOT NULL` una vez todos los `Grado` reales tengan su Facultad asignada. Nunca un `create_all()` directo contra una base con datos reales sin pasar por este backup-recreate-reimport -- protocolo ya aplicado una vez en este proyecto.
- **Sin capa Service**: la función del Router llama al repositorio directamente -- decisión ya cerrada en la discussion [#58](https://github.com/mmasias/pyCelda/discussions/58).
- **Validación de obligatoriedad por esquema de entrada**, no por paso explícito de la secuencia: `FacultadCreate` (Pydantic) exige `nombre` antes de que la función del Router se ejecute -- mismo mecanismo que `UniversidadCreate` un nivel arriba.
- **`201 Created`** con el objeto creado (incluido su `id`), no `204 No Content` -- la Vista navega de inmediato a `editarFacultad()` (`<<include>>` ya cerrado en Análisis) y necesita ese `id`.
- **Autorización de `Admin`: `Depends(require_admin)`** (dependencia fijada en el diseño de [`iniciarSesion()`](/RUP/03-diseño/casos-uso/iniciarSesion/README.md), no implementada en este documento) -- toda función de `routers/facultad.py` debe declararla explícitamente en Desarrollo. Especialmente relevante aquí por ser endpoint de escritura: el historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real.

## Referencias

- [`crearFacultad()` en Análisis](/RUP/02-analisis/casos-uso/crearFacultad/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearFacultad/README.md).
- [`crearUniversidad()` en Diseño](/RUP/03-diseño/casos-uso/crearUniversidad/README.md) -- mismo patrón de creación con `201` + `<<include>>`, un nivel arriba.
- [`editarFacultad()` en Diseño](/RUP/03-diseño/casos-uso/editarFacultad/README.md) -- destino del `<<include>>`.
- [`eliminarFacultad()` en Diseño](/RUP/03-diseño/casos-uso/eliminarFacultad/README.md) -- su consulta de bloqueo depende de la columna `facultad_id` fijada aquí.
