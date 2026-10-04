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
- **Versión**: 1.0
- **Fecha**: 2026-09-04
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`consultarEstadoActividadesFormativasMateria()`](/RUP/02-analisis/casos-uso/consultarEstadoActividadesFormativasMateria/README.md): un solo `GET` de solo lectura. El cálculo de la regla `AfM = Σ AfAdM` vive en `Materia.discrepancias_actividades_formativas()` (Fat Model, mismo sitio que `Guia.bloqueo_ponderaciones()`), no en el router ni en un servicio. **Código pendiente -- 🚧** (RUP escrito en el checkpoint del clúster; el endpoint y el método de dominio se construyen en el PR posterior, patrón #218/#224).

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/consultarEstadoActividadesFormativasMateria/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: sección "Actividades formativas de la materia" dentro de `AbrirMateriaView` (React) -- tabla de 10 filas (`horas` de la materia, `Σ` de las asignaturas, diferencia), resalta las que no cuadran, deja explícito que es informativo. `GET /api/v1/materias/{materia_id}/actividades-formativas/validacion`.
- **API**: `routers/materia.py::validar_actividades_formativas(materia_id)` -- auth `get_current_director_programa_id` + `_verificar_materia_del_director`. Solo lectura, no muta nada.
- **Modelo**: `Materia.discrepancias_actividades_formativas()` -- método de dominio; recorre las 10 `ActividadFormativaMateria` y, por cada una, suma las `horas` de las `ActividadFormativaAsignaturaPrograma` de sus `AsignaturaPrograma`.
- **Repositorio**: `MateriaRepository.obtener(materia_id)` con carga anticipada de la cascada (`ActividadFormativaMateria`, `AsignaturaPrograma` -> `ActividadFormativaAsignaturaPrograma`).

## Contrato de endpoint

### GET `/api/v1/materias/{materia_id}/actividades-formativas/validacion`

**Response (200 OK):** lista de 10 objetos, ordenados por `codigo`:
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

## Decisiones de diseño

- **Sub-recurso `/validacion` sobre la colección de actividades formativas de la `Materia`**, no un recurso propio: es una vista derivada del mismo agregado que sirve `editarActividadesFormativasMateria()`. `GET` puro, sin efectos.
- **Cálculo en el modelo, no en el router** (Fat Model sin Service, discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)): `Materia.discrepancias_actividades_formativas()` es análoga a `Guia.bloqueo_ponderaciones()` -- la diferencia es que aquí no hay ninguna acción que bloquear, el resultado es puramente informativo. El router solo serializa.
- **`cuadra` estricto (`diferencia == 0`)**: sin tolerancia -- `horas` es `Numeric(6, 2)`, la comparación es exacta. Si en la práctica molesta el redondeo se revisará, pero el requerimiento (discussion [#227](https://github.com/mmasias/pyCelda/discussions/227)) pide igualdad, no "aproximadamente".
- **No se valida la suma total contra ECTS** -- fuera de alcance por decisión de Manuel.
- **Se compone desde `abrirMateria()`**: la pantalla de detalle de `Materia` llama a este endpoint al abrir la sección; no hay navegación a una pantalla separada. Mismo patrón que `previsualizarGuia()` incrustado tras `abrirGuia()`.

## Referencias

- [`consultarEstadoActividadesFormativasMateria()` en Análisis](/RUP/02-analisis/casos-uso/consultarEstadoActividadesFormativasMateria/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoActividadesFormativasMateria/README.md).
- [`editarActividadesFormativasMateria()` en Diseño](/RUP/03-diseño/casos-uso/editarActividadesFormativasMateria/README.md) / [`editarActividadesFormativasAsignaturaPrograma()` en Diseño](/RUP/03-diseño/casos-uso/editarActividadesFormativasAsignaturaPrograma/README.md) -- los dos repartos que este medidor contrasta.
- [Discussion #58](https://github.com/mmasias/pyCelda/discussions/58) -- Fat Model sin capa Service.
