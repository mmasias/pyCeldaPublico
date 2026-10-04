<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarResultadoAprendizaje() > Desarrollo

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarResultadoAprendizaje/README.md)|[Análisis](/RUP/02-analisis/casos-uso/eliminarResultadoAprendizaje/README.md)|[Diseño](/RUP/03-diseño/casos-uso/eliminarResultadoAprendizaje/README.md)|**Desarrollo**|Pruebas|
> |-|-|-|-|-|-|-|

## Estado

✅ **Completado**

## Código

- **Router**: [`routers/resultado_aprendizaje.py`](/backend/app/routers/resultado_aprendizaje.py) -- `obtener_asignaciones(resultado_aprendizaje_id)`, `eliminar_resultado_aprendizaje(resultado_aprendizaje_id)`
- **Repositorio**: [`repositories/resultado_aprendizaje.py`](/backend/app/repositories/resultado_aprendizaje.py) -- `asignaciones()` y `nombres_asignaciones()` consultan las **dos** tablas de asociación (`materias_resultados_aprendizaje` y `asignaturas_programa_resultados_aprendizaje`); `eliminar()`
- **Modelo**: ninguno con lógica propia invocada -- borrado físico
- **Frontend**: Director `EliminarResultadoAprendizaje.tsx` (`/resultados-aprendizaje/:id/eliminar`); Admin `EliminarResultadoAprendizajeAdmin.tsx` (`/admin/resultados-aprendizaje/:id/eliminar`) -- cliente compartido en [`api.ts`](/frontend/src/api.ts) (mismos endpoints para ambos actores)
- **Tests**: [`tests/test_eliminar_resultado_aprendizaje.py`](/backend/tests/test_eliminar_resultado_aprendizaje.py) -- incluye las dos ramas bloqueadas (asignado a `Materia`, asignado solo a `AsignaturaPrograma`)

## Contrato de endpoint

### GET `/api/v1/resultados-aprendizaje/{resultado_aprendizaje_id}/asignaciones`

**Response (200 OK):**
```json
{ "materias": ["Programación I"], "asignaturas_programa": [] }
```

Listas vacías significan que se puede eliminar.

### DELETE `/api/v1/resultados-aprendizaje/{resultado_aprendizaje_id}`

**Response (204 No Content):** borrado físico.

**Response (409 Conflict, asignado a cualquier `Materia` o `AsignaturaPrograma`):**
```json
{ "detail": "ResultadoAprendizaje asignado a: <nombres de las asignaciones>" }
```

El bloqueo no vive solo en la Vista: aunque un cliente ignorara el `GET` de chequeo y disparara el `DELETE` directamente, el endpoint reconsulta `nombres_asignaciones()` y devuelve `409` -- la invariante se protege en el servidor.

**Response (404 Not Found):**
```json
{ "detail": "ResultadoAprendizaje no encontrado" }
```

### Autorización

`_verificar_resultado_del_director` (que delega en `_verificar_programa_del_director_o_admin`) -- Director del Programa o Admin (`get_current_admin_email_opcional`); sin Admin y sin dirigir el Programa, 404 uniforme. No hay endpoint `/api/v1/admin/...`.

## Referencias

- [`eliminarResultadoAprendizaje()` en Diseño](/RUP/03-diseño/casos-uso/eliminarResultadoAprendizaje/README.md) -- secuencia completa, decisiones de diseño.
