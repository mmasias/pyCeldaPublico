<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirProfesor() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirProfesor/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirProfesor/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-26
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`abrirProfesor()`](/RUP/02-analisis/casos-uso/abrirProfesor/README.md): un solo paso, de solo lectura, pero con una composición de respuesta que ningún detalle previo del catálogo tenía: además de `nombre`/`email`, la sección "Programas que dirige" -- los `Programa` del `DirectorPrograma` que comparte email con el `Profesor`. La respuesta es un `ProfesorDetalleResponse` que ensambla dos agregados (el `Profesor` y el rol resuelto por email), no la proyección plana de una fila.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirProfesor/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AbrirProfesorView` (React) -- pide `GET /api/v1/profesores/{profesor_id}`; presenta `nombre`/`email`, la tabla "Programas que dirige" con `[Quitar]` por fila y `[+ Nombrar director de Programa]`, más `[Editar]`/`[Volver al listado]`.
- **API**: `routers/profesor.py::obtener_profesor(profesor_id)` -- ensambla el detalle: `404` si el `Profesor` no existe; sin `DirectorPrograma` para ese email, `programas` queda vacía.
- **Modelo**: ninguno con lógica propia invocada -- el ensamblado del rol es trabajo del router con los repositorios.
- **Repositorio**: `ProfesorRepository.obtener(profesor_id)` + `DirectorProgramaRepository.obtener_por_email(email)` + `ProgramaRepository.listar_dirigidos_por(director_id)` -- este último ya existía: es el mismo método que alimenta `abrirProgramas()` del hilo `DirectorPrograma`.

## Decisiones de diseño

- **La relación `Profesor`-`DirectorPrograma` se resuelve por email en cada lectura** -- coherente con la decisión de `models/director_programa.py` (columna email denormalizada, sin joined-table inheritance): ningún endpoint necesita atravesar una jerarquía, solo emparejar. Coste asumido: cambiar el email de un `Profesor` desvincula su rol hasta que el `DirectorPrograma` se actualice -- documentado en [`editarProfesor()`](/RUP/03-diseño/casos-uso/editarProfesor/README.md).
- **`ProfesorDetalleResponse` con `programas` embebido** (`id`+`codigo`+`nombre` cada uno): la sección es parte del detalle en el wireframe, no una pantalla aparte -- un solo `GET` trae todo lo que `AbrirProfesorView` presenta.
- **`ProfesorResponse` (id+nombre+email) se reutiliza donde ya se usaba**: `AsignaturaPrograma.profesorado` y `GuiaResumenResponse.profesorado` ganan el campo `nombre` (nullable para las filas del seed aún sin backfill) -- ampliación aditiva, sin ruptura de consumidores.
- **Autorización de `Admin`: `Depends(require_admin)`**.
- **Sin capa Service**: Router delgado -> Repository.

## Referencias

- [`abrirProfesor()` en Análisis](/RUP/02-analisis/casos-uso/abrirProfesor/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirProfesor/README.md).
- [`quitarDirectorPrograma()` en Diseño](/RUP/03-diseño/casos-uso/quitarDirectorPrograma/README.md) / [`definirDirectorPrograma()` en Diseño](/RUP/03-diseño/casos-uso/definirDirectorPrograma/README.md) -- las acciones que viven en la sección que este detalle presenta.
- [`abrirMetodologiaDocente()` en Diseño](/RUP/03-diseño/casos-uso/abrirMetodologiaDocente/README.md) -- contraste: detalle de proyección plana de una fila.
