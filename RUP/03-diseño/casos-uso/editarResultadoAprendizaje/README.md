<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > editarResultadoAprendizaje() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarResultadoAprendizaje/README.md)|[Análisis](/RUP/02-analisis/casos-uso/editarResultadoAprendizaje/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-19
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`editarResultadoAprendizaje()`](/RUP/02-analisis/casos-uso/editarResultadoAprendizaje/README.md): sin `<<choice>>` -- edición de los tres campos (`codigo`, `tipo`, `descripcion`) sobre el formulario precargado. Traducción directa del `guardarCambios()` de Análisis: cargar por Repository, mutar en el Modelo (`actualizar()`), persistir por Repository.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/editarResultadoAprendizaje/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EditarResultadoAprendizajeView` (React) -- formulario precargado; pide `PUT /api/v1/resultados-aprendizaje/{resultado_aprendizaje_id}`. También destino del `<<include>>` de `crearResultadoAprendizaje()`.
- **API**: `routers/resultado_aprendizaje.py::editar_resultado_aprendizaje(resultado_aprendizaje_id, datos)` -- función suelta, sin capa Service.
- **Modelo**: `ResultadoAprendizaje.actualizar(codigo, tipo, descripcion)` -- aplica los tres campos sobre sí mismo, incluido `codigo` (editable aquí, a diferencia de `editarMetodologiaDocente()`).
- **Repositorio**: `ResultadoAprendizajeRepository.obtener(resultado_aprendizaje_id)` / `.actualizar(resultado_aprendizaje)`.

## Decisiones de diseño

- **Sin rama de fallo**: Análisis cierra el caso sin `<<choice>>` ni validación de negocio -- los tres campos son obligatorios de forma (Pydantic, `ResultadoAprendizajeUpdate`) y no hay invariante de estado que proteger; el `PUT` es un camino único.
- **Sin pantalla previa de carga propia**: el formulario llega precargado desde el estado del listado o del `<<include>>` -- el `GET` de carga es el de `abrirResultadoAprendizaje()`, no se duplica endpoint.

## Referencias

- [`editarResultadoAprendizaje()` en Análisis](/RUP/02-analisis/casos-uso/editarResultadoAprendizaje/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarResultadoAprendizaje/README.md).
- [`crearResultadoAprendizaje()` en Diseño](/RUP/03-diseño/casos-uso/crearResultadoAprendizaje/README.md) -- caso de uso que abre el `<<include>>` hacia este formulario.
