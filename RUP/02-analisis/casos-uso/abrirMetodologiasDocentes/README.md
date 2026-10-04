<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirMetodologiasDocentes()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiasDocentes/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirMetodologiasDocentes/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirMetodologiasDocentes()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiasDocentes/README.md): un solo paso, sin `<<choice>>`, de solo lectura. Presenta el listado completo de `MetodologiaDocente` -- catálogo institucional plano que cuelga directamente de `SISTEMA_DISPONIBLE` (entrada directa desde `abrirPanelAdministracion()`, sin composición padre, a diferencia de `Facultad` bajo `Universidad`), reutilizado por `Materia` y `AsignaturaPrograma` vía sus tablas de asociación. Cada fila muestra `codigo` y `descripcion`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirMetodologiasDocentes/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirMetodologiasDocentesView`

**Responsabilidades:**
- presenta el listado de `MetodologiaDocente`: `codigo`, `descripcion`.
- ofrece la navegación a abrir cada `MetodologiaDocente` y a crear una nueva (`[+ Crear Metodología Docente]`).

**Colaboraciones:**
- **Entrada:** `:SISTEMA_DISPONIBLE` -- el `Admin` solicita abrir Metodologías Docentes desde el panel de administración.
- **Control:** `MetodologiaDocenteController`.
- **Salida:** `:METODOLOGIAS_DOCENTES_ABIERTO`.

## Clases de controlador

### `MetodologiaDocenteController`

**Responsabilidades:**
- lista las `MetodologiaDocente` del catálogo (`listarMetodologiasDocentes()`).
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirMetodologiasDocentesView`.
- **Salida:** `MetodologiaDocenteRepository`.

## Clases de modelo

### `MetodologiaDocente`

**Responsabilidades:**
- porta `codigo` y `descripcion` -- los dos datos mostrados en cada fila del listado.

**Colaboraciones:**
- **Entrada:** listada por `MetodologiaDocenteRepository`.

### `MetodologiaDocenteRepository`

**Responsabilidades:**
- lista las `MetodologiaDocente` (`listar()`).

**Colaboraciones:**
- **Entrada:** `MetodologiaDocenteController`.
- **Salida:** gestiona `MetodologiaDocente`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiasDocentes/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiasDocentes/wireframes.puml) -- fuente de verdad del listado.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SISTEMA_DISPONIBLE --> METODOLOGIAS_DOCENTES_ABIERTO : abrirMetodologiasDocentes()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `MetodologiaDocente { codigo, descripcion }`, catálogo institucional reutilizado por `Materia` y `AsignaturaPrograma`.
- [`abrirMetodologiaDocente()`](../abrirMetodologiaDocente/README.md) / [`crearMetodologiaDocente()`](../crearMetodologiaDocente/README.md) / [`eliminarMetodologiaDocente()`](../eliminarMetodologiaDocente/README.md) -- casos de uso alcanzados desde el listado.
- [`abrirAsignaturas()`](../abrirAsignaturas/README.md) -- mismo patrón de listado plano sin composición padre, mismo `SISTEMA_DISPONIBLE` de entrada.
