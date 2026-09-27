<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > enviarGuiaARevision() > Desarrollo

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/enviarGuiaARevision/README.md)|[Análisis](/RUP/02-analisis/casos-uso/enviarGuiaARevision/README.md)|[Diseño](/RUP/03-diseño/casos-uso/enviarGuiaARevision/README.md)|**Desarrollo**|Pruebas|
> |-|-|-|-|-|-|-|

## Estado

✅ **Completado**

## Código

- **Router**: [`routers/guia.py`](/backend/app/routers/guia.py) -- `enviar_guia_a_revision(guia_id)` (`c1` 409, `c2` 422, `c3` 422)
- **Repositorio**: [`repositories/guia.py`](/backend/app/repositories/guia.py), [`repositories/ponderacion_evaluacion.py`](/backend/app/repositories/ponderacion_evaluacion.py), [`repositories/referencia_bibliografica.py`](/backend/app/repositories/referencia_bibliografica.py), [`repositories/sesion.py`](/backend/app/repositories/sesion.py) -- los cuatro con `existe_pendiente_de(guia_id)` (Bloque 2 de #206 añade `Sesion`)
- **Modelo**: [`models/guia.py`](/backend/app/models/guia.py) -- `bloqueo_ponderaciones()` (`c2`, issue #208), `planificacion_docente_completa()` / `sesiones_vinculadas_count()` (`c3`, Bloque 3 de #206), `enviar_a_revision()`
- **Tests**: [`tests/test_enviar_guia_a_revision.py`](/backend/tests/test_enviar_guia_a_revision.py)

## Contrato de endpoint

### POST `/api/v1/guias/{guia_id}/enviar-a-revision`

**Response (200 OK):**
```json
{
  "id": 1,
  "estado": "EnRevision",
  "fecha_ultima_modificacion": "2026-08-18T16:10:00"
}
```

**Response (409 Conflict, `c1` -- pendientes sin guardar):**
```json
{ "detail": "Hay items sin guardar -- guarda el borrador primero" }
```
Cubre `PonderacionEvaluacion`, `ReferenciaBibliografica` y `Sesion`.

**Response (422 Unprocessable Entity, `c2` -- rango o suma total incorrectos):**
```json
{ "detail": "Falta asignar 20% en Prácticas (mínimo 20%, asignado 0%)" }
```
El motivo concreto lo arma `Guia.bloqueo_ponderaciones()` (issue #208): recorre todos los `SistemaEvaluacion` de la materia, no solo los que ya tienen alguna `PonderacionEvaluacion` vinculada. Otras variantes del mismo `422`: `"Sobra N% en <tipo> (máximo M%, asignado X%)"` (por encima del máximo), o el genérico `"Rango por SistemaEvaluacion o suma total incorrectos"` si no hay ninguna ponderación vinculada o la suma total no es 100%.

**Response (422 Unprocessable Entity, `c3` -- planificación docente incompleta):**
```json
{ "detail": "Planificación docente incompleta: 18 de 25 sesiones" }
```

## Referencias

- [`enviarGuiaARevision()` en Diseño](/RUP/03-diseño/casos-uso/enviarGuiaARevision/README.md) -- secuencia completa, decisiones de diseño.
