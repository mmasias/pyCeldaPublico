<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarResultadoAprendizaje() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarResultadoAprendizaje/README.md)|[Análisis](/RUP/02-analisis/casos-uso/editarResultadoAprendizaje/README.md)|**Diseño**|Desarrollo|Pruebas|
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
- **Autorización: Director del Programa o Admin**: el endpoint es el mismo para ambos actores (sin espejo `/api/v1/admin/...`). El router resuelve la identidad con `get_current_director_programa_id_opcional` y `get_current_admin_email_opcional` y autoriza con `_verificar_resultado_del_director` (que delega en `_verificar_programa_del_director_o_admin`): con sesión Admin no exige dirigir el `Programa`; sin Admin, un `Programa` que no se dirige (o inexistente) responde 404 uniforme, sin distinguir "no existe" de "no es tuyo" (en los endpoints por resultado, el 404 es el de `ResultadoAprendizaje no encontrado`). La Vista de Admin es una pantalla propia (`*Admin.tsx`) sobre la misma llamada.

## Referencias

- [`editarResultadoAprendizaje()` en Análisis](/RUP/02-analisis/casos-uso/editarResultadoAprendizaje/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarResultadoAprendizaje/README.md).
- [`crearResultadoAprendizaje()` en Diseño](/RUP/03-diseño/casos-uso/crearResultadoAprendizaje/README.md) -- caso de uso que abre el `<<include>>` hacia este formulario.
