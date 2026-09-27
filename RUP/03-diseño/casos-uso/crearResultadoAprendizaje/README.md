<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > crearResultadoAprendizaje() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearResultadoAprendizaje/README.md)|[Análisis](/RUP/02-analisis/casos-uso/crearResultadoAprendizaje/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-19
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`crearResultadoAprendizaje()`](/RUP/02-analisis/casos-uso/crearResultadoAprendizaje/README.md): sin patrón C→U y sin `<<choice>>` -- los tres campos (`codigo`, `tipo`, `descripcion`) se piden de una vez y la creación es real e inmediata. Un solo `POST` al Repository, sin método de Modelo intermedio ni rama de fallo: no hay regla de negocio que validar más allá de la obligatoriedad de la forma.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/crearResultadoAprendizaje/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `CrearResultadoAprendizajeView` (React) -- formulario con `codigo`, `tipo`, `descripcion`; pide `POST /api/v1/grados/{grado_id}/resultados-aprendizaje` y navega a `editarResultadoAprendizaje()` (`<<include>>`).
- **API**: `routers/resultado_aprendizaje.py::crear_resultado_aprendizaje(grado_id, datos)` -- función suelta, sin capa Service.
- **Modelo**: ninguno con lógica propia invocada -- el `ResultadoAprendizaje` nace con los tres datos ya fijados; no hay invariante que proteger.
- **Repositorio**: `ResultadoAprendizajeRepository.crear(grado_id, codigo, tipo, descripcion)` -- `INSERT` inmediato.

## Decisiones de diseño

- **Sin método de Modelo**: Análisis no introduce ningún `ResultadoAprendizaje.crear()` ni validación de negocio -- el Repository construye la fila directamente. Diseño traduce eso tal cual: Router -> Repository, sin paso por el Modelo.
- **La obligatoriedad de los tres campos la resuelve Pydantic**: `ResultadoAprendizajeCreate` (schemas/) rechaza el request antes de ejecutar la función del router -- mismo mecanismo ya documentado para `crearPonderacionEvaluacion()`/`crearReferenciaBibliografica()`, validación de forma resuelta por el framework.
- **201 Created**, siguiendo el código ya usado por `crearPonderacionEvaluacion()` para las creaciones inmediatas.

## Referencias

- [`crearResultadoAprendizaje()` en Análisis](/RUP/02-analisis/casos-uso/crearResultadoAprendizaje/README.md) -- diagrama de colaboración origen, incluida la ausencia de C→U (issue [#24](https://github.com/mmasias/pyCelda/issues/24)).
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearResultadoAprendizaje/README.md).
- [`editarResultadoAprendizaje()` en Diseño](/RUP/03-diseño/casos-uso/editarResultadoAprendizaje/README.md) -- destino del `<<include>>`.
