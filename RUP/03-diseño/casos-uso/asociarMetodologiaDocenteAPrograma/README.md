<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > asociarMetodologiaDocenteAPrograma() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAPrograma/README.md)|[Análisis](/RUP/02-analisis/casos-uso/asociarMetodologiaDocenteAPrograma/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-10-03
- **Autor**: Claude Sonnet 5.5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`asociarMetodologiaDocenteAPrograma()`](/RUP/02-analisis/casos-uso/asociarMetodologiaDocenteAPrograma/README.md): sin `<<choice>>` -- primer nivel de la cadena `MetodologiaDocente`. Agregación simple (`Programa o-- MetodologiaDocente`, sin clase de asociación). A diferencia del nivel inferior ([`asociarMetodologiaDocenteAAsignaturaPrograma()`](/RUP/03-diseño/casos-uso/asociarMetodologiaDocenteAAsignaturaPrograma/README.md)), no hay regla de subconjunto: el universo es el catálogo institucional de la `Universidad` del `Programa`. `ProgramaController` converge en `routers/programa.py`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/asociarMetodologiaDocenteAPrograma/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AsociarMetodologiaDocenteAProgramaView` (React) -- selector del catálogo no asociado; pide `GET .../disponibles` y `POST /api/v1/programas/{programa_id}/metodologias-docentes`.
- **API**: `routers/programa.py::listar_metodologias_docentes_disponibles_para_programa(programa_id)` / `::asociar_metodologia_docente_a_programa(programa_id, datos)` -- funciones sueltas; ambas pasan por `_verificar_programa_del_director()`.
- **Modelo**: `Programa` gana una `MetodologiaDocente` en su colección -- sin método invocado; `MetodologiaDocente` porta `codigo`/`descripcion`.
- **Repositorio**: `MetodologiaDocenteRepository.listar_disponibles_para_programa(programa_id)` -- `LEFT JOIN` con la tabla intermedia y filtro por `universidad_id`; `ProgramaRepository.asociar_metodologia_docente(programa_id, metodologia_docente_id)` -- `INSERT` en `programas_metodologias_docentes`.

## Decisiones de diseño

- **Filtro por `Universidad` en la consulta de disponibles**: el catálogo es por `Universidad` (issue [#655](https://github.com/mmasias/pyCelda/issues/655)), así que `disponibles` ofrece solo las de la `Universidad` del `Programa` que aún no tiene. Análisis lo expresaba como "aún no asociadas"; el filtro por `Universidad` es una precisión de Diseño.
- **El `POST` revalida la `Universidad`** (`exigir_metodologia_de_la_universidad()`, 409 `La MetodologiaDocente pertenece a otra Universidad -- no se puede asociar`): a diferencia del selector, el endpoint no confía en que el cliente solo ofrezca opciones válidas. No hay otra invariante de estado que proteger.
- **`ProgramaRepository` persiste su tabla intermedia** (`programas_metodologias_docentes`), mismo criterio que `AsignaturaProgramaRepository` en el nivel inferior -- sin clase de asociación no hay repositorio propio de la tabla.
- **Un único endpoint para `DirectorPrograma` y `Admin`**: a diferencia de los casos de `AsignaturaPrograma` (endpoint espejo bajo `/api/v1/admin/...`), aquí las dependencias son `get_current_director_programa_id_opcional` + `get_current_admin_email_opcional` y `_verificar_programa_del_director()` deja pasar a `Admin` sin comprobar propiedad. La secuencia es idéntica con `Admin` como actor.
- **204 No Content**: agregación simple, sin entidad nueva que devolver.

## Referencias

- [`asociarMetodologiaDocenteAPrograma()` en Análisis](/RUP/02-analisis/casos-uso/asociarMetodologiaDocenteAPrograma/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAPrograma/README.md).
- [`asociarMetodologiaDocenteAAsignaturaPrograma()` en Diseño](/RUP/03-diseño/casos-uso/asociarMetodologiaDocenteAAsignaturaPrograma/README.md) -- plantilla estructural; contraste: allí hay regla de subconjunto y endpoint espejo `Admin`.
- [`asociarMetodologiaDocenteAMateria()` en Diseño](/RUP/03-diseño/casos-uso/asociarMetodologiaDocenteAMateria/README.md) -- nivel siguiente de la cadena.
- [`desasociarMetodologiaDocentePrograma()` en Diseño](/RUP/03-diseño/casos-uso/desasociarMetodologiaDocentePrograma/README.md) -- caso de uso complementario.
