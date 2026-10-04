<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > importarActividadesFormativasDeAsignaturaProgramaPrima()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/importarActividadesFormativasDeAsignaturaProgramaPrima/README.md)|**Análisis**|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`importarActividadesFormativasDeAsignaturaProgramaPrima()`](/RUP/01-requisitos/03-detalle-casos-uso/importarActividadesFormativasDeAsignaturaProgramaPrima/README.md): el `DirectorPrograma` copia el reparto de las 10 `ActividadFormativaAsignaturaPrograma` de una `AsignaturaPrograma` **prima** (misma `Materia`, issue [#529](https://github.com/mmasias/pyCelda/issues/529)) sobre la `AsignaturaPrograma` que tiene abierta. Reemplazo total **in place** (`actualizar(horas, porcentajePresencialidad)`, sin borrar y recrear), real e inmediato, sin efecto sobre ninguna `Guia` y sin `HistorialCambio`. Las candidatas excluyen la propia y las primas sin configurar (10 filas a 0), y se ordenan por proximidad de créditos.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/importarActividadesFormativasDeAsignaturaProgramaPrima/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `ImportarActividadesFormativasDeAsignaturaProgramaPrimaView`

**Responsabilidades:**
- presenta las primas configuradas con `nombre`, `ects` y `totalHoras`, junto a los créditos de la destino.
- permite solicitar importar desde una prima, con confirmación previa del reemplazo total.
- estado vacío sin botón activo si no hay candidatas.

**Colaboraciones:**
- **Entrada:** `:ASIGNATURA_PROGRAMA_ABIERTO`.
- **Control:** `AsignaturaProgramaController`.
- **Salida:** `:ASIGNATURA_PROGRAMA_ABIERTO` -- self-loop, ya con el reparto importado.

## Clases de controlador

### `AsignaturaProgramaController`

**Responsabilidades:**
- `listarPrimasImportables(asignaturaProgramaId)`: primas con alguna hora configurada, ordenadas por `abs(ects_prima - ects_destino)` y luego por nombre.
- `validarPrima(destino, origen)`: revalidación server-side; el origen debe estar entre las primas configuradas de la destino, y si no, 404 uniforme. El id del cliente nunca se confía.
- `importarActividadesFormativas(asignaturaProgramaId, origenAsignaturaProgramaId)`: actualiza in place las 10 filas de la destino con los valores del origen, en un solo commit.

**Colaboraciones:**
- **Entrada:** `ImportarActividadesFormativasDeAsignaturaProgramaPrimaView`.
- **Salida:** `AsignaturaProgramaRepository`, `ActividadFormativaAsignaturaProgramaRepository`, `ActividadFormativaAsignaturaPrograma`.

## Clases de modelo

### `AsignaturaPrograma`

**Responsabilidades:**
- porta `materiaId`: dos `AsignaturaPrograma` con el mismo `materiaId` son primas.

### `AsignaturaProgramaRepository`

**Responsabilidades:**
- `listarPrimas(asignaturaProgramaId)`: otras `AsignaturaPrograma` de la misma `Materia`, excluyendo la propia; `[]` si no hay ninguna.

### `ActividadFormativaAsignaturaPrograma`

**Responsabilidades:**
- `actualizar(horas, porcentajePresencialidad)`: la misma operación que usa `editarActividadesFormativasAsignaturaPrograma()`.

### `ActividadFormativaAsignaturaProgramaRepository`

**Responsabilidades:**
- `listarDe(asignaturaProgramaId)`: las 10 filas, en orden AF1..AF10; `actualizarLote(...)` persiste el resultado.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/importarActividadesFormativasDeAsignaturaProgramaPrima/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/importarActividadesFormativasDeAsignaturaProgramaPrima/wireframes.puml).
- [`editarActividadesFormativasAsignaturaPrograma()`](../editarActividadesFormativasAsignaturaPrograma/README.md) -- misma operación con valores tecleados.
- [`importarBibliografiaDeGuiaHermana()`](../importarBibliografiaDeGuiaHermana/README.md) -- plantilla de formato.
- [Issue #529](https://github.com/mmasias/pyCelda/issues/529), [issue #530](https://github.com/mmasias/pyCelda/issues/530).
