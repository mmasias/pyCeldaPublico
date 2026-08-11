<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > generarGuiasPDF()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/generarGuiasPDF/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Selección|Bloqueada (pendientes)|Generada (éxito)|
|:-:|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/generarGuiasPDF/wireframe-seleccion.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/generarGuiasPDF/wireframe-bloqueada.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/generarGuiasPDF/wireframe-generada.svg)|
|||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Generar los PDF de todas las `Guia` `Aprobada` de un `Grado` en un `CursoAcademico`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Self-loop de `SISTEMA_DISPONIBLE`, sin pasar por `GRADO_ABIERTO` -- a diferencia de [`reabrirGuiaPorIncidencia()`](../reabrirGuiaPorIncidencia/README.md), no hereda contexto de una navegación previa por grado, así que el propio formulario resuelve la selección de `Grado`+`CursoAcademico` (verbo `selecciona`, cuarto verbo del vocabulario cerrado -- ambas entidades ya existen, no son dato nuevo). Apuntado para más adelante, fuera de alcance de L9: reubicar la llamada a un contexto que ya resuelva `Grado` -- ver discussion [#44](https://github.com/mmasias/pyCelda/discussions/44), punto 3.

**`<<choice>>` bloqueante**: todas las `Guia` de `(Grado, CursoAcademico)` deben estar `Aprobada`; si falta alguna, bloquea sin generar nada y lista las pendientes. Formaliza el disparador narrado en el guión de eventos ("cuando todas las guías del grado están Aprobada... genera las guías en PDF") como un evento discreto sobre un conjunto completo, no una generación parcial -- descartada por no tener evidencia en el guión de eventos, mismo criterio que ya excluyó acciones en bloque no evidenciadas (ver [catálogo de actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md)). Nota aparte, ya apuntada en la discussion [#33](https://github.com/mmasias/pyCelda/discussions/33): esto valida solo el **estado** (`Aprobada`), no la **completitud de contenido** (profesorado/RA/MD/`SistemaEvaluacion` ponderados) -- sigue fuera de alcance.

Postcondición: `fechaGeneracionPDF` se actualiza en cada `Guia` del `Grado` generada -- mismo atributo que [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md) consulta para decidir si ofrece el botón de descarga.

Datos del wireframe: pantalla **bloqueada** con dato real, sin hipótesis -- `GII__IYA003` realmente `Borrador`, motivo real del bloqueo. Pantalla **generada** con la misma `Guia` mostrada hipotéticamente `Aprobada` (necesaria para ilustrar el camino de éxito, documentado igual que el resto del lote en la discussion #44).

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SISTEMA_DISPONIBLE --> SISTEMA_DISPONIBLE : generarGuiasPDF()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catálogo de casos de uso de `Admin` sobre `Guia`
- Modelo del dominio -- guión de eventos, `fechaGeneracionPDF`
- [`notificarGuiasActualizadas()`](../notificarGuiasActualizadas/README.md) -- aviso del `DirectorGrado` que dispara este caso de uso
- [Discussion #33](https://github.com/mmasias/pyCelda/discussions/33) -- validación de completitud de contenido, fuera de alcance
- [Discussion #44](https://github.com/mmasias/pyCelda/discussions/44) -- cierre de L9, punto 3
