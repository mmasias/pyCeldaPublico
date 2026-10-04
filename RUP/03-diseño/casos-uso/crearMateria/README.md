<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearMateria() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearMateria/README.md)|[Análisis](/RUP/02-analisis/casos-uso/crearMateria/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-25
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`crearMateria()`](/RUP/02-analisis/casos-uso/crearMateria/README.md): CRUD real e inmediato contra `MateriaRepository`, sin capa Service. Un único paso, sin `<<choice>>` -- el formulario de Requisitos pide un solo campo obligatorio (`nombre`), resuelto por esquema de entrada (Pydantic), no por una llamada explícita en la secuencia. La creación vive anidada bajo `Programa` (`Programa *-- Materia`, composición), con `programa_id` en la URL y no en el body (`POST /api/v1/admin/programas/{programa_id}/materias`, mismo patrón que `POST /api/v1/admin/facultades/{facultad_id}/programas` del lote anterior).

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/crearMateria/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `CrearMateriaAdmin.tsx` (React, ruta `/admin/programas/{programa_id}/materias/crear`) -- formulario mínimo (`nombre`, sin selector de Programa: llega de la URL); al confirmar, `POST /api/v1/admin/programas/{programa_id}/materias`.
- **API**: `routers/materia.py::crear_materia(programa_id, datos)` -- función suelta, sin capa Service; delega directo en el repositorio.
- **Modelo**: `Materia` (SQLAlchemy) -- sin lógica propia invocada: el Repository construye la fila directamente; sin `estado` que fijar (`Materia` no se extingue).
- **Repositorio**: `MateriaRepository.crear(nombre, programa_id)` -- método nuevo sobre el repositorio ya existente del hilo `Guia`/asociaciones; persistencia real e inmediata.

## Decisiones de diseño

- **Namespace propio `/api/v1/admin/programas/{programa_id}/materias`, separado de `/api/v1/programas/{programa_id}/materias`** (ya existente para `DirectorPrograma`, con `Depends(get_current_director_programa_id)`) -- mismo motivo que separó `/api/v1/admin/facultades/{facultad_id}/programas` de `/api/v1/programas`: cada guard en su sitio, sin condicionales por rol dentro de una misma función. Ambos endpoints convergen en el mismo `MateriaRepository.listar_del_programa()`.
- **Validación de obligatoriedad por esquema de entrada**: `MateriaCreate` (Pydantic) exige `nombre` antes de que la función del Router se ejecute -- `validarDatosObligatorios(nombre)` de Análisis se disuelve en Pydantic, mismo hallazgo ya documentado en el diagrama de clases de Diseño (discussion [#60](https://github.com/mmasias/pyCelda/discussions/60)).
- **`201 Created` con el objeto creado (incluido su `id`)**, no `204 No Content` -- la Vista navega de inmediato a `editarMateria()` (`<<include>>` cerrado en Análisis) y necesita ese `id`.
- **Autorización de `Admin`: `Depends(require_admin)`** -- ya disponible en `backend/app/core/auth.py`. Especialmente relevante aquí por ser endpoint de escritura: el historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real.
- **Sin capa Service**: Router delgado -> Repository, sin validación post-consulta.

## Referencias

- [`crearMateria()` en Análisis](/RUP/02-analisis/casos-uso/crearMateria/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearMateria/README.md).
- [`crearPrograma()` en Diseño](/RUP/03-diseño/casos-uso/crearPrograma/README.md) -- mismo patrón de creación anidada con `201` + `<<include>>`, el precedente directo de la rebanada anterior.
- [`crearUniversidad()` en Diseño](/RUP/03-diseño/casos-uso/crearUniversidad/README.md) -- el patrón nombre-only original.
- [`editarMateria()` en Diseño](/RUP/03-diseño/casos-uso/editarMateria/README.md) -- destino del `<<include>>`.
- [`abrirMaterias()` en Diseño](/RUP/03-diseño/casos-uso/abrirMaterias/README.md) -- listado Admin que sirve de punto de entrada, con su variante Admin construida en este mismo lote.
