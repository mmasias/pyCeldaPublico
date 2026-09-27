<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > abrirAsignaturasGrado() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturasGrado/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirAsignaturasGrado/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-19
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`abrirAsignaturasGrado()`](/RUP/02-analisis/casos-uso/abrirAsignaturasGrado/README.md), en su variante `DirectorGrado`: listado agregado por `Grado`, de solo lectura -- fusiona las `AsignaturaGrado` del `Grado` (con su profesorado) con el estado de su `Guia` del curso activo, reutilizando `GuiaRepository.listar_del_grado(grado_id)` tal cual (método ya existente desde `consultarEstadoGuias()`, del hilo `Guia` L7-L9).

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirAsignaturasGrado/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AbrirAsignaturasGradoView` (React) -- pide `GET /api/v1/grados/{grado_id}/asignaturas-grado`; presenta asignatura, materia, curso, carácter, profesorado y estado de la `Guia`.
- **API**: `routers/asignatura_grado.py::listar_asignaturas_grado_del_grado(grado_id)` -- función suelta; fusiona ambos listados en memoria (agregación de lectura, sin regla de negocio).
- **Modelo**: ninguno con lógica propia invocada -- `AsignaturaGrado` y `Guia` solo portan los datos de cada fila.
- **Repositorio**: `AsignaturaGradoRepository.listar_del_grado(grado_id)` (método nuevo, con profesorado por relación) / `GuiaRepository.listar_del_grado(grado_id)` -- **reutilizado tal cual**, sin Repository nuevo para este caso de uso.

## Decisiones de diseño

- **`GuiaRepository.listar_del_grado()` se reutiliza, no se duplica**: es la decisión explícita de Análisis y la condición del encargo -- el estado de las `Guia` ya tiene su consulta agregada desde `consultarEstadoGuias()`; aquí solo se consume.
- **Dos consultas y fusión en el Router**, no un `JOIN` único: los dos listados llegan de repositorios distintos (tablas sin relación directa entre sí más allá de la fusión visual); el Router los casa en memoria por `asignatura_grado_id` -- mismo mecanismo que `abrirGuia()` etiquetó como `API -> API: fusiona ...`.
- **`routers/asignatura_grado.py`, no `routers/guia.py`**: aunque una de las dos fuentes sea `Guia`, el recurso que sirve el endpoint es `AsignaturaGrado` -- el módulo se elige por el agregado de la respuesta, mismo criterio que `consultarEstadoGuias()` eligió `guia.py` porque su recurso era el estado de las `Guia`.
- **`AsignaturaGradoConEstadoGuiaResponse`**: fila de `AsignaturaGrado` + `estado_guia` (o ausencia) -- la fusión es de presentación, no del modelo.

## Referencias

- [`abrirAsignaturasGrado()` en Análisis](/RUP/02-analisis/casos-uso/abrirAsignaturasGrado/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturasGrado/README.md).
- [`consultarEstadoGuias()` en Diseño](/RUP/03-diseño/casos-uso/consultarEstadoGuias/README.md) -- origen de `GuiaRepository.listar_del_grado()`.
- [`abrirAsignaturaGrado()` en Diseño](/RUP/03-diseño/casos-uso/abrirAsignaturaGrado/README.md) -- destino `[Abrir]` de cada fila de este listado.
