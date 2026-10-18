<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarActividadFormativa() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarActividadFormativa/README.md)|[Análisis](/RUP/02-analisis/casos-uso/eliminarActividadFormativa/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 2.0
- **Fecha**: 2026-10-17
- **Autor**: Claude (vía Claude Code)

## Propósito

Bajada a diseño de [`eliminarActividadFormativa()`](/RUP/02-analisis/casos-uso/eliminarActividadFormativa/README.md) (issue [#772](https://github.com/mmasias/pyCelda/issues/772)): un único `DELETE` que resuelve el `<<choice>>` y el borrado; el bloqueo sale como `409` con los nombres de las `Materia` en el `detail`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/eliminarActividadFormativa/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EliminarActividadFormativa` (React), prop `admin` -- carga con `GET /api/v1/actividades-formativas/{id}`, confirma con `DELETE`; un `409` pasa la pantalla a la rama bloqueada con el `detail` tal cual.
- **API**: `routers/actividad_formativa.py::eliminar_actividad_formativa(actividad_formativa_id)`, `_autorizar_actividad()`.
- **Repositorio**: `ActividadFormativaRepository.nombres_materias_asociadas()`, `eliminar()`.

## Decisiones de diseño

- **Un solo endpoint, sin `GET` de chequeo previo**: lista vacía de `nombres_materias_asociadas()` procede al borrado (`204`); no vacía, `409` con `"ActividadFormativa asignada a: ..."`. La invariante queda protegida en el servidor aunque un cliente dispare el `DELETE` a ciegas.
- **"En uso" = horas > 0, no mera existencia de fila**: `nombres_materias_asociadas()` une las `Materia` con horas > 0 en `ActividadFormativaMateria` y las `Materia` de las `AsignaturaPrograma` con horas > 0 en `ActividadFormativaAsignaturaPrograma`, sin repetir y ordenadas.
- **Al borrar, se retiran antes las filas a 0** de las dos tablas de asociación, para no dejar FKs colgando; todo en una transacción.
- **Autorización compartida Admin/Director** por el `Programa` de la actividad; `404` uniforme fuera de alcance.
- **La rama "cancelada" no genera llamada HTTP**.
- **Sin capa Service**: Router delgado -> Repository (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).
- **Histórico**: hasta #772, `Depends(require_admin)` y catálogo de `Universidad`; la consulta de uso y el borrado de filas a 0 son los mismos desde #655.

## Referencias

- [`eliminarActividadFormativa()` en Análisis](/RUP/02-analisis/casos-uso/eliminarActividadFormativa/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/eliminarActividadFormativa/README.md).
- [`eliminarCompetencia()` en Diseño](/RUP/03-diseño/casos-uso/eliminarCompetencia/README.md) -- contraste: consulta previa de asignaciones.
