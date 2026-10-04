<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearCursoAcademico() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearCursoAcademico/README.md)|[Análisis](/RUP/02-analisis/casos-uso/crearCursoAcademico/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-09-21
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`crearCursoAcademico()`](/RUP/02-analisis/casos-uso/crearCursoAcademico/README.md): CRUD real e inmediato contra `CursoAcademicoRepository`, sin capa Service. Un único paso, sin `<<choice>>`: la obligatoriedad de `inicio`/`fin` se resuelve por esquema de entrada (Pydantic, tipo `date`), no por una llamada explícita en la secuencia.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/crearCursoAcademico/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `CrearCursoAcademicoView` (React) -- formulario mínimo (`inicio`, `fin`); al confirmar, `POST /api/v1/admin/cursos-academicos`. **Sin pantalla propia en esta rebanada** (ver Desarrollo) -- este documento describe el diseño completo del caso de uso, independiente de qué parte se materializó ya en código.
- **API**: `routers/curso_academico.py::crear_curso_academico(datos)` -- función suelta, sin capa Service; delega directo en el repositorio.
- **Modelo**: `CursoAcademico` (SQLAlchemy) -- sin lógica propia invocada: el Repository construye la fila directamente a partir de los campos del formulario; `estado` nace `"Inactivo"` por `default` de columna, no por una asignación explícita del Repository.
- **Repositorio**: `CursoAcademicoRepository.crear(inicio, fin)` -- persistencia real e inmediata.

## Decisiones de diseño

- **Esquema nuevo: `cursos_academicos`**, tabla enteramente nueva y sin relación de composición con ninguna otra tabla todavía -- `Base.metadata.create_all()` la crea al arrancar el backend sin tocar tablas existentes (SQLite solo crea tablas ausentes, nunca altera una ya existente), mismo mecanismo que `historial_cambios` (issue #392, tabla nueva sin script `migrar_*.py` dedicado): no hace falta uno para dar de alta una tabla nueva sin columnas que añadir a tablas ya existentes -- a diferencia de `facultades`/`Programa.facultad_id`, donde sí hizo falta uno.
- **Sin capa Service**: la función del Router llama al repositorio directamente -- decisión ya cerrada en la discussion [#58](https://github.com/mmasias/pyCelda/discussions/58).
- **Validación de obligatoriedad por esquema de entrada**, no por paso explícito de la secuencia: `CursoAcademicoCreate` (Pydantic, `inicio: date`/`fin: date`) exige ambos campos y el formato ISO-8601 antes de que la función del Router se ejecute -- mismo mecanismo que `FacultadCreate`.
- **Sin validación de `inicio < fin` ni de solapamiento entre cursos**: no está especificada en la ficha de Requisitos -- no se inventa una restricción que no pidió Manuel. Si se necesita, es un issue aparte.
- **`201 Created`** con el objeto creado (incluido su `id`), no `204 No Content` -- la Vista, cuando exista, navegaría de inmediato a `editarCursoAcademico()` (`<<include>>` ya cerrado en Análisis) y necesita ese `id`.
- **Autorización de `Admin`: `Depends(require_admin)`** (dependencia fijada en el diseño de [`iniciarSesion()`](/RUP/03-diseño/casos-uso/iniciarSesion/README.md), no implementada en este documento) -- toda función de `routers/curso_academico.py` debe declararla explícitamente en Desarrollo, mismo criterio que el resto de endpoints de escritura de `Admin`.
- **`semestre_activo` nullable, sin setter en esta rebanada**: columna presente en el modelo porque ya forma parte del modelo de dominio (`CursoAcademico.semestreActivo`), pero `activarSemestre()` no está en el alcance de este CU -- ni de la segunda mitad de #222.

## Referencias

- [`crearCursoAcademico()` en Análisis](/RUP/02-analisis/casos-uso/crearCursoAcademico/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearCursoAcademico/README.md).
- [`crearFacultad()` en Diseño](/RUP/03-diseño/casos-uso/crearFacultad/README.md) -- mismo patrón de creación con `201` + `<<include>>`, plantilla de este documento.
- [`editarCursoAcademico()`](/RUP/01-requisitos/03-detalle-casos-uso/editarCursoAcademico/README.md) -- destino del `<<include>>`, sin Diseño propio todavía.
