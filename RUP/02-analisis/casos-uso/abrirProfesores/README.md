<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > abrirProfesores()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirProfesores/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirProfesores/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirProfesores()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirProfesores/README.md): un solo paso, sin `<<choice>>`, de solo lectura. Presenta el listado completo de `Profesor` -- catálogo institucional top-level que cuelga directamente de `SISTEMA_DISPONIBLE` (entrada directa desde `abrirPanelAdministracion()`, sin composición padre, como `MetodologiaDocente`), reutilizado por `AsignaturaGrado` vía su tabla de asociación `profesorado`. Cada fila muestra `nombre` y `email`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirProfesores/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirProfesoresView`

**Responsabilidades:**
- presenta el listado de `Profesor`: `nombre`, `email`.
- ofrece la navegación a abrir cada `Profesor`, a eliminarlo (`[Eliminar]` por fila) y a crear uno nuevo (`[+ Crear Profesor]`).

**Colaboraciones:**
- **Entrada:** `:SISTEMA_DISPONIBLE` -- el `Admin` solicita abrir Profesores desde el panel de administración.
- **Control:** `ProfesorController`.
- **Salida:** `:PROFESORES_ABIERTO`.

## Clases de controlador

### `ProfesorController`

**Responsabilidades:**
- lista los `Profesor` del catálogo (`listarProfesores()`).
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirProfesoresView`.
- **Salida:** `ProfesorRepository`.

## Clases de modelo

### `Profesor`

**Responsabilidades:**
- porta `nombre` y `email` -- los dos datos mostrados en cada fila del listado.

**Colaboraciones:**
- **Entrada:** listada por `ProfesorRepository`.

### `ProfesorRepository`

**Responsabilidades:**
- lista los `Profesor` (`listar()`).

**Colaboraciones:**
- **Entrada:** `ProfesorController`.
- **Salida:** gestiona `Profesor`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirProfesores/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirProfesores/wireframes.puml) -- fuente de verdad del listado.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SISTEMA_DISPONIBLE --> PROFESORES_ABIERTO : abrirProfesores()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Profesor -u-|> Actor`, catálogo independiente reutilizado por `AsignaturaGrado.profesorado`.
- [`abrirProfesor()`](../abrirProfesor/README.md) / [`crearProfesor()`](../crearProfesor/README.md) / [`eliminarProfesor()`](../eliminarProfesor/README.md) -- casos de uso alcanzados desde el listado.
- [`abrirMetodologiasDocentes()`](../abrirMetodologiasDocentes/README.md) -- mismo patrón de listado plano sin composición padre, mismo `SISTEMA_DISPONIBLE` de entrada.
