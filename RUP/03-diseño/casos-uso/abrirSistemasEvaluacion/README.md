<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirSistemasEvaluacion() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirSistemasEvaluacion/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirSistemasEvaluacion/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-26
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`abrirSistemasEvaluacion()`](/RUP/02-analisis/casos-uso/abrirSistemasEvaluacion/README.md): un solo paso, de solo lectura. Presenta el listado de `SistemaEvaluacion` de una `Materia` -- composición real, no catálogo plano: la URL anida bajo la `Materia`, mismo criterio que los `ResultadoAprendizaje` bajo su `Programa`. `SistemaEvaluacionController` converge en `routers/sistema_evaluacion.py`, módulo nuevo de funciones sueltas que absorbe los 5 CU del CRUD.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirSistemasEvaluacion/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `SistemasEvaluacion` (React, ruta `/admin/materias/:materiaId/sistemas-evaluacion`) -- pide `GET /api/v1/admin/materias/{materia_id}/sistemas-evaluacion`; presenta `tipo`, `descripcion` y el rango de ponderación mínima--máxima por fila, con `[Abrir]`/`[Eliminar]` por fila, `[+ Crear]` y `[Volver a la materia]`.
- **API**: `routers/sistema_evaluacion.py::listar_sistemas_evaluacion_de_materia(materia_id)` -- función suelta, primera del módulo nuevo.
- **Modelo**: ninguno con lógica propia invocada -- `SistemaEvaluacion` solo porta los datos de cada fila.
- **Repositorio**: `SistemaEvaluacionRepository.listar_de_materia(materia_id)` -- un solo `SELECT` filtrado por `materia_id`. El repositorio ya existía con `obtener()` (usado por el hilo `PonderacionEvaluacion`); gana aquí sus primeros métodos de catálogo propio.

## Decisiones de diseño

- **Ruta anidada bajo la `Materia`**: el listado pertenece a la composición de la `Materia` (`Materia *-- SistemaEvaluacion`), la URL refleja esa propiedad -- mismo criterio que `listar_resultados_aprendizaje_del_programa()` colgó de `/programas/{programa_id}`.
- **Namespace `/admin/` en el listado, por colisión con un contrato ya cerrado**: el path natural `/api/v1/materias/{materia_id}/sistemas-evaluacion` ya existe -- es el selector de `crearPonderacionEvaluacion()`/`editarPonderacionEvaluacion()` (routers/ponderacion_evaluacion.py), con autorización de `Profesor` y contrato documentado en su fase de Desarrollo. Un endpoint no puede registrar dos guardas distintas: la variante `Admin` cuelga de `/api/v1/admin/materias/{materia_id}/sistemas-evaluacion` con `require_admin`, misma convención de doble namespace que ya usan las variantes Admin de `Programa`/`Materia` (`/api/v1/admin/programas/{programa_id}/materias` frente a `/api/v1/programas/{programa_id}/materias`). Mismos datos, misma forma de respuesta; solo cambia quién puede llamarlo.
- **Autorización de `Admin`: `Depends(require_admin)`** -- composición real que gestiona `Admin`, sin pertenencia de `DirectorPrograma` que verificar. El historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real.
- **`404` si la `Materia` no existe** -- guardia de Router sobre el `None` de `MateriaRepository.obtener()`, mismo mensaje que el endpoint del picker.
- **Módulo `routers/sistema_evaluacion.py` nuevo**: crecerá con `obtener_sistema_evaluacion()`, `crear_sistema_evaluacion()`, `editar_sistema_evaluacion()` y `eliminar_sistema_evaluacion()` de los CU hermanos.
- **Sin capa Service**: Router delgado -> Repository (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).

## Referencias

- [`abrirSistemasEvaluacion()` en Análisis](/RUP/02-analisis/casos-uso/abrirSistemasEvaluacion/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirSistemasEvaluacion/README.md).
- [`abrirResultadosAprendizaje()` en Diseño](/RUP/03-diseño/casos-uso/abrirResultadosAprendizaje/README.md) -- precedente de listado anidado bajo un padre.
- [`crearPonderacionEvaluacion()` en Desarrollo](/RUP/04-desarrollo/casos-uso/crearPonderacionEvaluacion/README.md) -- contrato ya cerrado del endpoint gemelo de `Profesor` que motiva el namespace `/admin/`.
