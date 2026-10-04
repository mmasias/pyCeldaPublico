<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearPonderacionEvaluacion() > Desarrollo

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearPonderacionEvaluacion/README.md)|[Análisis](/RUP/02-analisis/casos-uso/crearPonderacionEvaluacion/README.md)|[Diseño](/RUP/03-diseño/casos-uso/crearPonderacionEvaluacion/README.md)|**Desarrollo**|Pruebas|
> |-|-|-|-|-|-|-|

## Estado

✅ **Completado**

## Código

- **Router**: [`routers/ponderacion_evaluacion.py`](/backend/app/routers/ponderacion_evaluacion.py) -- `listar_sistemas_evaluacion(materia_id)`, `crear_ponderacion_evaluacion(guia_id, datos)`
- **Repositorio**: [`repositories/materia.py`](/backend/app/repositories/materia.py), [`repositories/sistema_evaluacion.py`](/backend/app/repositories/sistema_evaluacion.py), [`repositories/ponderacion_evaluacion.py`](/backend/app/repositories/ponderacion_evaluacion.py)
- **Modelo**: [`models/materia.py`](/backend/app/models/materia.py), [`models/sistema_evaluacion.py`](/backend/app/models/sistema_evaluacion.py)
- **Schema**: [`schemas/ponderacion_evaluacion.py`](/backend/app/schemas/ponderacion_evaluacion.py), [`schemas/sistema_evaluacion.py`](/backend/app/schemas/sistema_evaluacion.py)
- **Tests**: [`tests/test_crear_ponderacion_evaluacion.py`](/backend/tests/test_crear_ponderacion_evaluacion.py)

## Contrato de endpoint

### GET `/api/v1/materias/{materia_id}/sistemas-evaluacion`

**Response (200 OK):**
```json
[
  {
    "id": 3,
    "tipo": "Evaluación continua",
    "descripcion": "Prácticas",
    "ponderacion_minima": 20.0,
    "ponderacion_maxima": 60.0
  }
]
```

### POST `/api/v1/guias/{guia_id}/ponderaciones-evaluacion`

**Request:**
```json
{
  "sistema_evaluacion_id": 3,
  "descripcion": "Examen parcial",
  "ponderacion": 30
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "guia_id": 1,
  "sistema_evaluacion_id": 3,
  "descripcion": "Examen parcial",
  "ponderacion": 30.0,
  "vinculada": false
}
```

**Response (422 Unprocessable Entity, ponderación > máximo del sistema):**
```json
{ "detail": "La ponderación supera el máximo del SistemaEvaluacion" }
```

## Referencias

- [`crearPonderacionEvaluacion()` en Diseño](/RUP/03-diseño/casos-uso/crearPonderacionEvaluacion/README.md) -- secuencia completa, decisiones de diseño.
