<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirMetodologiasDocentesPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiasDocentesPrograma/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirMetodologiasDocentesPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirMetodologiasDocentesPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiasDocentesPrograma/README.md): un solo paso, sin `<<choice>>`, de solo lectura. Presenta el catálogo de `MetodologiaDocente` propio del `Programa` -- metodologías del catálogo institucional asociadas al `Programa` (`Programa -- MetodologiaDocente (asociación)`).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirMetodologiasDocentesPrograma/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirMetodologiasDocentesProgramaView`

**Responsabilidades:**
- presenta el catálogo de `MetodologiaDocente` del `Programa`: `codigo`, `descripcion`.
- ofrece la navegación a desasociar cada una y a asociar una nueva.

**Colaboraciones:**
- **Entrada:** `:PROGRAMA_ABIERTO` -- el actor (`Admin` o `DirectorPrograma`) solicita abrir el catálogo de `MetodologiaDocente` del `Programa`.
- **Control:** `MetodologiaDocenteController`.
- **Salida:** `:METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO`.

## Clases de controlador

### `MetodologiaDocenteController`

**Responsabilidades:**
- lista los `MetodologiaDocente` de un `Programa` (`listarMetodologiasDocentesDelPrograma(programaId)`).
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirMetodologiasDocentesProgramaView`.
- **Salida:** `MetodologiaDocenteRepository`.

## Clases de modelo

### `MetodologiaDocente`

**Responsabilidades:**
- porta `codigo`, `descripcion` -- los datos mostrados en cada fila del listado.

**Colaboraciones:**
- **Entrada:** listado por `MetodologiaDocenteRepository`.

### `MetodologiaDocenteRepository`

**Responsabilidades:**
- lista los `MetodologiaDocente` de un `Programa` (`listarDelPrograma(programaId)`).

**Colaboraciones:**
- **Entrada:** `MetodologiaDocenteController`.
- **Salida:** gestiona `MetodologiaDocente`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiasDocentesPrograma/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiasDocentesPrograma/wireframes.puml) -- fuente de verdad del contenido presentado.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROGRAMA_ABIERTO --> METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO : abrirMetodologiasDocentesPrograma()`.
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `PROGRAMA_ABIERTO --> METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO : abrirMetodologiasDocentesPrograma()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa -- MetodologiaDocente (asociación)`.
- [`asociarMetodologiaDocenteAPrograma()`](../asociarMetodologiaDocenteAPrograma/README.md) y [`desasociarMetodologiaDocentePrograma()`](../desasociarMetodologiaDocentePrograma/README.md) -- casos de uso alcanzados desde esta pantalla.
