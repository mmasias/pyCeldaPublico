<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarProfesor() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarProfesor/README.md)|[Análisis](/RUP/02-analisis/casos-uso/eliminarProfesor/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-26
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`eliminarProfesor()`](/RUP/02-analisis/casos-uso/eliminarProfesor/README.md): `<<choice>>` bloqueante -- borrado físico del catálogo institucional. La especificación enuncia tres motivos; el diseño comprueba tres condiciones reales, independientes: (1) `AsignaturaPrograma` asignadas -- estado en vivo, tabla `asignaturas_programa_profesores`; (2) `Guia` que referencian al `Profesor` -- tabla propia `guias_profesores`, poblada por copia puntual al crear la `Guia`, **no** derivada de (1); y (3) rol de `DirectorPrograma` activo -- existe `DirectorPrograma` con su email y dirige al menos un `Programa`. El `409` lleva los motivos presentes en el `detail`, una frase por condición.

**Cierra el issue #13 de verdad, resuelto en el pipeline de `asignarProfesorAAsignaturaPrograma()`/`desasignarProfesorAsignaturaPrograma()`**: el issue [#13](https://github.com/mmasias/pyCelda/issues/13) (cerrado) pide bloqueo *permanente* por historial -- un `Profesor` que alguna vez impartió una `Guia` no debería poder borrarse físicamente nunca, aunque se le desasigne antes, por riesgo real sobre la generación de actas de cursos anteriores (razón explícita de Manuel al cerrar el issue). Al escribir esta pieza (PR #137) eso no se cumplía: `Guia.profesorado` era una `@property` derivada en vivo de `AsignaturaPrograma.profesorado`, así que `desasignarProfesorAsignaturaPrograma()` seguido de `eliminarProfesor()` borraba físicamente sin bloqueo. `Guia.profesorado` es ahora relación M2M propia (`guias_profesores`), nunca tocada por `desasignarProfesorAsignaturaPrograma()` -- la condición (2) de arriba es justo lo que cierra el issue.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/eliminarProfesor/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EliminarProfesorView` (React) -- carga la información con `GET /api/v1/profesores/{profesor_id}` y pide confirmar/cancelar; si la confirmación recibe `409`, presenta la rama bloqueada con el `detail` tal cual (los motivos).
- **API**: `routers/profesor.py::eliminar_profesor(profesor_id)` -- función suelta, un único endpoint que resuelve el `<<choice>>` y el borrado.
- **Modelo**: ninguno con lógica propia invocada -- sin `estado` propio que mutar, el borrado es físico.
- **Repositorio**: `ProfesorRepository.motivos_bloqueo_eliminacion(profesor_id)` (tres queries independientes: `asignaturas_programa_profesores` con join a `AsignaturaPrograma` para los nombres; `guias_profesores` con join a `Guia`/`AsignaturaPrograma` para el historial; resolución del `DirectorPrograma` por email y `listar_dirigidos_por()` para los `Programa`) / `.eliminar(profesor_id)`.

## Decisiones de diseño

- **Un solo endpoint, sin `GET` de chequeo previo** (mismo patrón que `eliminarMetodologiaDocente()`): el `<<choice>>` se resuelve dentro del propio `DELETE` -- lista vacía de motivos procede al borrado (`204`), lista no vacía devuelve `409` con `detail="Profesor asignado a: AsignaturaPrograma 'X', ...; dirige: Programa 'Y', ..."`. La invariante queda protegida en el servidor aunque un cliente dispare el `DELETE` a ciegas: el endpoint reconsulta antes de borrar.
- **Dos motivos en la misma lista, no tres comprobaciones** -- decisión verificada contra el código, no una simplificación: `Guia.profesorado` es `self.asignatura_programa.profesorado` -- la misma relación M2M, no una tercera fuente independiente. Un `Profesor` sin `AsignaturaPrograma` asignadas no puede aparecer en ninguna `Guia`; comprobar `asignaturas_programa_profesores` una vez cubre ambos enunciados de Requisitos.
- **"Rol de DirectorPrograma activo" = dirige al menos un `Programa`** -- no basta con que exista la fila `DirectorPrograma` con su email: tras varios `quitarDirectorPrograma()` puede quedar un `DirectorPrograma` huérfano (que sigue resolviendo el login) que no bloquea el borrado.
- **`motivos_bloqueo_eliminacion()` devuelve frases, no un booleano** -- mismo patrón que `nombres_materias_asociadas()`/`nombres_asignaciones()` de encargos anteriores, pero con tres tipos de motivo en la misma lista: la lista vacía es el booleano (puede eliminarse) y los nombres alimentan el `detail` del `409`.
- **La fila `DirectorPrograma` no se toca al borrar el `Profesor`**: el rol vive en su propia tabla por email (denormalizada); un `DirectorPrograma` sin `Profesor` asociado sigue resolviendo el login -- eliminarlo en cascada cambiaría semántica de autenticación que este CU no pide.
- **`204 No Content` para el `DELETE`**: borrado físico, no hay entidad que devolver -- la Vista vuelve al listado.
- **La rama "cancelada" no genera llamada HTTP**: se modela como rama del `alt` para reflejar las tres salidas de Análisis, pero sin tocar el backend.
- **`404` si el identificador no existe** -- guardia de Router sobre el `None` del repositorio.
- **Autorización de `Admin`: `Depends(require_admin)`** -- endpoint de borrado, explícito.
- **Sin capa Service**: Router delgado -> Repository.

## Referencias

- [`eliminarProfesor()` en Análisis](/RUP/02-analisis/casos-uso/eliminarProfesor/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/eliminarProfesor/README.md) -- los tres motivos enunciados y la nota del bloqueo permanente por `Guia` histórica (issue #13).
- [`eliminarMetodologiaDocente()` en Diseño](/RUP/03-diseño/casos-uso/eliminarMetodologiaDocente/README.md) -- mismo patrón de endpoint único sin chequeo previo; allí una sola tabla que comprobar, aquí tres consultas independientes.
- [`quitarDirectorPrograma()` en Diseño](/RUP/03-diseño/casos-uso/quitarDirectorPrograma/README.md) / [`desasignarProfesorAsignaturaPrograma()` en Diseño](/RUP/03-diseño/casos-uso/desasignarProfesorAsignaturaPrograma/README.md) -- las acciones que deshacen dos de los tres motivos; el de `Guia` (historial) es permanente.
