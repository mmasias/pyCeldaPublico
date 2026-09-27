<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > abrirAsignaturaGrado() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturaGrado/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirAsignaturaGrado/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-19
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`abrirAsignaturaGrado()`](/RUP/02-analisis/casos-uso/abrirAsignaturaGrado/README.md): un solo paso, de solo lectura, con dos entradas (`GRADO_ABIERTO` y `MATERIA_ABIERTO`) que comparten un único flujo -- un `GET` por identificador resuelve ambas. Presenta los 9 atributos propios (`requisitosPrevios` incluido, discussion [#259](https://github.com/mmasias/pyCelda/discussions/259)) y sus tres colecciones asociadas: profesorado, `MetodologiaDocente` y `ResultadoAprendizaje`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirAsignaturaGrado/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AbrirAsignaturaGradoView` (React) -- pide `GET /api/v1/asignaturas-grado/{asignatura_grado_id}`; presenta datos propios, profesorado, `MetodologiaDocente` y `ResultadoAprendizaje` asociados.
- **API**: `routers/asignatura_grado.py::obtener_asignatura_grado(asignatura_grado_id)` -- función suelta.
- **Modelo**: ninguno con lógica propia invocada -- `AsignaturaGrado`, `MetodologiaDocente`, `ResultadoAprendizaje` y `Profesor` portan los datos presentados.
- **Repositorio**: `AsignaturaGradoRepository.obtener(asignatura_grado_id)` / `.listar_metodologias_docentes_de(asignatura_grado_id)` / `.listar_resultados_aprendizaje_de(asignatura_grado_id)` / `.listar_profesorado_de(asignatura_grado_id)` -- cuatro métodos sobre el mismo agregado.

## Decisiones de diseño

- **Las dos entradas de Análisis colapsan en un endpoint**: tanto si se llega desde `GRADO_ABIERTO` como desde `MATERIA_ABIERTO`, la Vista ya conoce el `asignatura_grado_id` de la fila pulsada -- no hace falta parámetro de contexto ni endpoint por entrada; los dos retornos (`abrirGrado()` y `abrirMateria()`) también son decisión de navegación del cliente -- `materia_id` ya viaja en `AsignaturaGradoDetalleResponse`, sin dato ni endpoint nuevo.
- **La variante `Admin` gana el mismo segundo retorno** (issue [#252](https://github.com/mmasias/pyCelda/issues/252)): `AsignaturaGradoAdmin.tsx` navega a `MateriaAdmin.tsx` (`/admin/materias/{materia_id}`) donde `AsignaturaGrado.tsx` navega a `Materia.tsx` (`/materias/{materia_id}`) -- misma mecánica, sin dato ni endpoint nuevo. Cierra la asimetría que el retoque de `DirectorGrado` (2026-09-04) había abierto, segunda oleada del patrón de reversión sobre uso real.
- **Los tres listados firma el mismo `AsignaturaGradoRepository`**: a diferencia de los selectores de disponibles (que consultan el agregado devuelto), aquí las tres colecciones cuelgan del agregado abierto -- Análisis ya lo asignaba así, evitando dispersar tres lecturas de una misma pantalla por tres repositorios.
- **El profesorado es de solo lectura**: la gestión de `Profesor` en `AsignaturaGrado` es exclusiva de `Admin` (fuera de alcance, discussion [#65](https://github.com/mmasias/pyCelda/discussions/65)) -- se lista, sin endpoint de mutación en este lote.

## Referencias

- [`abrirAsignaturaGrado()` en Análisis](/RUP/02-analisis/casos-uso/abrirAsignaturaGrado/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturaGrado/README.md).
- [`abrirMateria()` en Diseño](/RUP/03-diseño/casos-uso/abrirMateria/README.md) -- patrón de detalle con colecciones, sobre el agregado vecino.
- [`editarAsignaturaGrado()` en Diseño](/RUP/03-diseño/casos-uso/editarAsignaturaGrado/README.md) -- edición de los datos propios que esta pantalla presenta.
- [`editarActividadesFormativasAsignaturaGrado()` en Diseño](/RUP/03-diseño/casos-uso/editarActividadesFormativasAsignaturaGrado/README.md) -- el clúster de `ActividadFormativa` (discussion [#227](https://github.com/mmasias/pyCelda/discussions/227)) suma la sección "Actividades formativas" (rejilla de `horas` + `porcentaje_presencialidad`); `AsignaturaGradoDetalleResponse` gana el campo al construir el clúster, con audit del agregado `AsignaturaGrado`.
