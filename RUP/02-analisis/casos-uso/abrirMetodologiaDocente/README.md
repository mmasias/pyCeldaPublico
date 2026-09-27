<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > abrirMetodologiaDocente()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiaDocente/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirMetodologiaDocente/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirMetodologiaDocente()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiaDocente/README.md): un solo paso, sin `<<choice>>`, de solo lectura. Presenta los datos de la `MetodologiaDocente` (`codigo`, `descripcion`) y ofrece editar o volver al listado. `MetodologiaDocente` no tiene composición debajo -- a diferencia de `Universidad`/`Facultad`, desde aquí no se navega a ningún catálogo hijo, solo a la edición del propio detalle.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirMetodologiaDocente/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirMetodologiaDocenteView`

**Responsabilidades:**
- presenta el `codigo` y la `descripcion` de la `MetodologiaDocente`.
- ofrece la navegación a editar y a volver al listado (`[Editar]`/`[Volver al listado]`).

**Colaboraciones:**
- **Entrada:** `:METODOLOGIAS_DOCENTES_ABIERTO` -- el `Admin` solicita abrir una `MetodologiaDocente` del listado.
- **Control:** `MetodologiaDocenteController`.
- **Salida:** `:METODOLOGIA_DOCENTE_ABIERTO`.

## Clases de controlador

### `MetodologiaDocenteController`

**Responsabilidades:**
- recupera la `MetodologiaDocente` (`cargarMetodologiaDocente(metodologiaDocenteId)`).
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirMetodologiaDocenteView`.
- **Salida:** `MetodologiaDocenteRepository`.

## Clases de modelo

### `MetodologiaDocente`

**Responsabilidades:**
- porta `codigo` y `descripcion` -- los datos mostrados en el detalle.

**Colaboraciones:**
- **Entrada:** recuperada por `MetodologiaDocenteRepository`.

### `MetodologiaDocenteRepository`

**Responsabilidades:**
- recupera la `MetodologiaDocente` por identificador (`obtener(metodologiaDocenteId)`).

**Colaboraciones:**
- **Entrada:** `MetodologiaDocenteController`.
- **Salida:** gestiona `MetodologiaDocente`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiaDocente/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiaDocente/wireframes.puml) -- fuente de verdad del contenido presentado.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `METODOLOGIAS_DOCENTES_ABIERTO --> METODOLOGIA_DOCENTE_ABIERTO : abrirMetodologiaDocente()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `MetodologiaDocente { codigo, descripcion }`.
- [`abrirMetodologiasDocentes()`](../abrirMetodologiasDocentes/README.md) -- listado desde el que se alcanza este caso de uso.
- [`editarMetodologiaDocente()`](../editarMetodologiaDocente/README.md) -- destino del botón `[Editar]`.
- [`abrirAsignatura()`](../abrirAsignatura/README.md) -- mismo patrón de detalle de solo lectura.
