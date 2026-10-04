<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirAsignaturaPrograma() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturaPrograma/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirAsignaturaPrograma/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-19
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`abrirAsignaturaPrograma()`](/RUP/02-analisis/casos-uso/abrirAsignaturaPrograma/README.md): un solo paso, de solo lectura, con dos entradas (`PROGRAMA_ABIERTO` y `MATERIA_ABIERTO`) que comparten un único flujo -- un `GET` por identificador resuelve ambas. Presenta los 9 atributos propios (`requisitosPrevios` incluido, discussion [#259](https://github.com/mmasias/pyCelda/discussions/259)) y sus tres colecciones asociadas: profesorado, `MetodologiaDocente` y `ResultadoAprendizaje`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirAsignaturaPrograma/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AbrirAsignaturaProgramaView` (React) -- pide `GET /api/v1/asignaturas-programa/{asignatura_programa_id}`; presenta datos propios, profesorado, `MetodologiaDocente` y `ResultadoAprendizaje` asociados.
- **API**: `routers/asignatura_programa.py::obtener_asignatura_programa(asignatura_programa_id)` -- función suelta.
- **Modelo**: ninguno con lógica propia invocada -- `AsignaturaPrograma`, `MetodologiaDocente`, `ResultadoAprendizaje` y `Profesor` portan los datos presentados.
- **Repositorio**: `AsignaturaProgramaRepository.obtener(asignatura_programa_id)` / `.listar_metodologias_docentes_de(asignatura_programa_id)` / `.listar_resultados_aprendizaje_de(asignatura_programa_id)` / `.listar_profesorado_de(asignatura_programa_id)` -- cuatro métodos sobre el mismo agregado.

## Decisiones de diseño

- **Las dos entradas de Análisis colapsan en un endpoint**: tanto si se llega desde `PROGRAMA_ABIERTO` como desde `MATERIA_ABIERTO`, la Vista ya conoce el `asignatura_programa_id` de la fila pulsada -- no hace falta parámetro de contexto ni endpoint por entrada; los dos retornos (`abrirPrograma()` y `abrirMateria()`) también son decisión de navegación del cliente -- `materia_id` ya viaja en `AsignaturaProgramaDetalleResponse`, sin dato ni endpoint nuevo.
- **La variante `Admin` gana el mismo segundo retorno** (issue [#252](https://github.com/mmasias/pyCelda/issues/252)): `AsignaturaProgramaAdmin.tsx` navega a `MateriaAdmin.tsx` (`/admin/materias/{materia_id}`) donde `AsignaturaPrograma.tsx` navega a `Materia.tsx` (`/materias/{materia_id}`) -- misma mecánica, sin dato ni endpoint nuevo. Cierra la asimetría que el retoque de `DirectorPrograma` (2026-09-04) había abierto, segunda oleada del patrón de reversión sobre uso real.
- **Los tres listados firma el mismo `AsignaturaProgramaRepository`**: a diferencia de los selectores de disponibles (que consultan el agregado devuelto), aquí las tres colecciones cuelgan del agregado abierto -- Análisis ya lo asignaba así, evitando dispersar tres lecturas de una misma pantalla por tres repositorios.
- **El profesorado es de solo lectura**: la gestión de `Profesor` en `AsignaturaPrograma` es exclusiva de `Admin` (fuera de alcance, discussion [#65](https://github.com/mmasias/pyCelda/discussions/65)) -- se lista, sin endpoint de mutación en este lote.

## Referencias

- [`abrirAsignaturaPrograma()` en Análisis](/RUP/02-analisis/casos-uso/abrirAsignaturaPrograma/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturaPrograma/README.md).
- [`abrirMateria()` en Diseño](/RUP/03-diseño/casos-uso/abrirMateria/README.md) -- patrón de detalle con colecciones, sobre el agregado vecino.
- [`editarAsignaturaPrograma()` en Diseño](/RUP/03-diseño/casos-uso/editarAsignaturaPrograma/README.md) -- edición de los datos propios que esta pantalla presenta.
- [`editarActividadesFormativasAsignaturaPrograma()` en Diseño](/RUP/03-diseño/casos-uso/editarActividadesFormativasAsignaturaPrograma/README.md) -- el clúster de `ActividadFormativa` (discussion [#227](https://github.com/mmasias/pyCelda/discussions/227)) suma la sección "Actividades formativas" (rejilla de `horas` + `porcentaje_presencialidad`); `AsignaturaProgramaDetalleResponse` gana el campo al construir el clúster, con audit del agregado `AsignaturaPrograma`.
