<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > consultarEstadoActividadesFormativasMateria() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoActividadesFormativasMateria/README.md)|[Análisis](/RUP/02-analisis/casos-uso/consultarEstadoActividadesFormativasMateria/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 2.0
- **Fecha**: 2026-10-17
- **Autor**: Claude (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`consultarEstadoActividadesFormativasMateria()`](/RUP/02-analisis/casos-uso/consultarEstadoActividadesFormativasMateria/README.md): solo lectura, dos lecturas. El cálculo de la regla `AfM = Σ AfAdM` vive en `Materia.discrepancias_actividades_formativas()` (endpoint `/validacion`) y la comprobación por ECTS en `Materia.comprobacion_horas_ects()` (campo `comprobacion_horas_ects` del detalle de la `Materia`, issue [#772](https://github.com/mmasias/pyCelda/issues/772)); los dos en el modelo (Fat Model, mismo sitio que `Guia.bloqueo_ponderaciones()`), no en el router ni en un servicio.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/consultarEstadoActividadesFormativasMateria/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: secciones "Actividades formativas de la materia" y "Estado de las actividades formativas" dentro de la ficha de `Materia` (React, `Materia.tsx`) -- línea "Horas de la materia: N de M (E ECTS a 25 h)" con OK o la discrepancia, y tabla con una fila por actividad del catálogo (`horas` de la materia, `Σ` de las asignaturas, estado); resalta lo que no cuadra y deja explícito que es informativo. `GET /api/v1/materias/{materia_id}` (comprobación por ECTS) y `GET /api/v1/materias/{materia_id}/actividades-formativas/validacion` (discrepancias).
- **API**: `routers/materia.py::validar_actividades_formativas_materia(materia_id)` y `::obtener_materia(materia_id)` (con `_datos_ruct(materia)`: `codigo_ruct`, `ects`, `comprobacion_horas_ects`) -- auth `get_current_director_programa_id` + `_verificar_materia_del_director`. Solo lectura, no muta nada.
- **Modelo**: `Materia.discrepancias_actividades_formativas()` -- recorre las `ActividadFormativaMateria` (una por actividad del catálogo del `Programa`) y, por cada una, suma las `horas` de las `ActividadFormativaAsignaturaPrograma` de sus `AsignaturaPrograma`. `Materia.comprobacion_horas_ects()` -- suma las `horas` de sus `ActividadFormativaMateria` y las compara con `ects × HORAS_POR_ECTS` (25); `None` sin `ects`.
- **Repositorio**: `MateriaRepository.obtener(materia_id)` con carga anticipada de la cascada (`ActividadFormativaMateria`, `AsignaturaPrograma` -> `ActividadFormativaAsignaturaPrograma`).

## Contrato de endpoint

### GET `/api/v1/materias/{materia_id}/actividades-formativas/validacion`

**Response (200 OK):** una fila por actividad del catálogo del `Programa`, en orden de alta:
```json
{
  "codigo": "AF2",
  "nombre": "Clases prácticas",
  "horas_materia": 20.0,
  "horas_asignaturas": 15.0,
  "cuadra": false,
  "diferencia": -5.0
}
```
`diferencia = horas_asignaturas - horas_materia`; `cuadra = (diferencia == 0)`.

**Response (404 Not Found):** `Materia` inexistente o no dirigida por el `DirectorPrograma`.

### GET `/api/v1/materias/{materia_id}` -- campo `comprobacion_horas_ects`

```json
{ "ects": 6.0, "horas_esperadas": 150.0, "horas_materia": 140.0, "cuadra": false, "diferencia": -10.0 }
```

`diferencia = horas_materia - horas_esperadas`, redondeado a 2 decimales; `cuadra = (diferencia == 0)`. `null` si la `Materia` no tiene `ects`.

## Decisiones de diseño

- **Sub-recurso `/validacion` sobre la colección de actividades formativas de la `Materia`**, no un recurso propio: es una vista derivada del mismo agregado que sirve `editarActividadesFormativasMateria()`. `GET` puro, sin efectos.
- **Cálculo en el modelo, no en el router** (Fat Model sin Service, discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)): `Materia.discrepancias_actividades_formativas()` es análoga a `Guia.bloqueo_ponderaciones()` -- la diferencia es que aquí no hay ninguna acción que bloquear, el resultado es puramente informativo. El router solo serializa.
- **`cuadra` estricto (`diferencia == 0`)**: sin tolerancia -- `horas` es `Numeric(6, 2)`, la comparación es exacta. Si en la práctica molesta el redondeo se revisará, pero el requerimiento (discussion [#227](https://github.com/mmasias/pyCelda/discussions/227)) pide igualdad, no "aproximadamente".
- **Comprobación por ECTS en el detalle de la `Materia`, no en `/validacion`** (#772): es un dato de la materia, no de cada actividad; viaja con `ects` y `codigo_ruct` en `_datos_ruct()` y lo reciben las dos fichas (Director y Admin) sin endpoint nuevo. Se compara contra `Materia.ects` (dato aprobado de la memoria), no contra la suma de ECTS de sus `AsignaturaPrograma`, que por optatividad puede ser mayor. No reparte nada (reparto proporcional descartado en #768). Hasta #772 no había comprobación por ECTS (la `Materia` no tenía `ects`).
- **Se compone desde `abrirMateria()`**: la pantalla de detalle de `Materia` llama a este endpoint al abrir la sección; no hay navegación a una pantalla separada. Mismo patrón que `previsualizarGuia()` incrustado tras `abrirGuia()`.

**Actor `Admin` (issue [#755](https://github.com/mmasias/pyCelda/issues/755))**: endpoint espejo `GET /api/v1/admin/materias/{id}/actividades-formativas/validacion`, con `require_admin`; el cálculo sigue en `Materia.discrepancias_actividades_formativas()`. La comprobación por ECTS llega en `GET /api/v1/admin/materias/{id}` (`MateriaAdminDetalleResponse`).


## Referencias

- [`consultarEstadoActividadesFormativasMateria()` en Análisis](/RUP/02-analisis/casos-uso/consultarEstadoActividadesFormativasMateria/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoActividadesFormativasMateria/README.md).
- [`editarActividadesFormativasMateria()` en Diseño](/RUP/03-diseño/casos-uso/editarActividadesFormativasMateria/README.md) / [`editarActividadesFormativasAsignaturaPrograma()` en Diseño](/RUP/03-diseño/casos-uso/editarActividadesFormativasAsignaturaPrograma/README.md) -- los dos repartos que este medidor contrasta.
- [Discussion #58](https://github.com/mmasias/pyCelda/discussions/58) -- Fat Model sin capa Service.
