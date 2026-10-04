<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirResultadosAprendizaje() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirResultadosAprendizaje/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirResultadosAprendizaje/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-19
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`abrirResultadosAprendizaje()`](/RUP/02-analisis/casos-uso/abrirResultadosAprendizaje/README.md): un solo paso, sin `<<choice>>`, de solo lectura. `ResultadoAprendizajeController` (B/C/E) converge en `routers/resultado_aprendizaje.py` con una única función de listado -- primer endpoint del módulo, puerta de entrada al CRUD del catálogo de `ResultadoAprendizaje` del `Programa`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirResultadosAprendizaje/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AbrirResultadosAprendizajeView` (React) -- pide `GET /api/v1/programas/{programa_id}/resultados-aprendizaje`; presenta `codigo`, `tipo`, `descripcion` por fila.
- **API**: `routers/resultado_aprendizaje.py::listar_resultados_aprendizaje_del_programa(programa_id)` -- función suelta, sin capa Service.
- **Modelo**: ninguno con lógica propia invocada -- `ResultadoAprendizaje` solo porta los datos de cada fila.
- **Repositorio**: `ResultadoAprendizajeRepository.listar_del_programa(programa_id)` -- un solo `SELECT` filtrado por `programa_id`.

## Decisiones de diseño

- **Ruta anidada bajo `/programas/{programa_id}`**: el catálogo pertenece al `Programa` (`Programa *-d- ResultadoAprendizaje`, composición con descendencia), no es un catálogo institucional plano -- la URL refleja esa propiedad, mismo criterio que `listar_sistemas_evaluacion()` colgó de `/materias/{materia_id}`.
- **Módulo `routers/resultado_aprendizaje.py` nuevo**: absorbe los 5 CU del catálogo de `ResultadoAprendizaje` (abrir listado, abrir detalle, crear, editar, eliminar) -- uno por función suelta, sin clase Controller.
- **Sin capa Service**: Router delgado -> Repository; caso de uso de solo lectura sin método de Modelo que invocar.
- **Autorización: Director del Programa o Admin**: el endpoint es el mismo para ambos actores (sin espejo `/api/v1/admin/...`). El router resuelve la identidad con `get_current_director_programa_id_opcional` y `get_current_admin_email_opcional` y autoriza con ``_verificar_programa_del_director_o_admin``: con sesión Admin no exige dirigir el `Programa`; sin Admin, un `Programa` que no se dirige (o inexistente) responde 404 uniforme, sin distinguir "no existe" de "no es tuyo". La Vista de Admin es una pantalla propia (`*Admin.tsx`) sobre la misma llamada.

## Referencias

- [`abrirResultadosAprendizaje()` en Análisis](/RUP/02-analisis/casos-uso/abrirResultadosAprendizaje/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirResultadosAprendizaje/README.md).
- [`consultarEstadoGuias()` en Diseño](/RUP/03-diseño/casos-uso/consultarEstadoGuias/README.md) -- precedente de endpoint de listado por `Programa`.
