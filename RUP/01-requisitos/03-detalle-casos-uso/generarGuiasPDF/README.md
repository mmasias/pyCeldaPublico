<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

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
|**Objetivo**|Generar los PDF de todas las `Guia` `Aprobada` de un `Programa` en un `CursoAcademico`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Self-loop de `SISTEMA_DISPONIBLE`, sin pasar por `PROGRAMA_ABIERTO` -- a diferencia de [`reabrirGuiaPorIncidencia()`](../reabrirGuiaPorIncidencia/README.md), no hereda contexto de una navegación previa por programa, así que el propio formulario resuelve la selección de `Programa`+`CursoAcademico` (verbo `selecciona`, cuarto verbo del vocabulario cerrado -- ambas entidades ya existen, no son dato nuevo). Apuntado para más adelante, fuera de alcance de L9: reubicar la llamada a un contexto que ya resuelva `Programa` -- ver discussion [#44](https://github.com/mmasias/pyCelda/discussions/44), punto 3.

**No implementado en código -- caso de uso solo de la fase de Requisitos.** Mismo régimen que `Requisito`/`CursoAcademico` en el modelo del dominio: representación correcta, pendiente de construir. No existe ningún endpoint de generación de PDFs en ningún router del backend.

**`<<choice>>` bloqueante**: todas las `Guia` de `(Programa, CursoAcademico)` deben estar `Aprobada`; si falta alguna, bloquea sin generar nada y lista las pendientes. Formaliza el disparador narrado en el [guión de eventos](/RUP/00-modelo-del-dominio/README.md) ("cuando todas las guías del programa están Aprobada... genera las guías en PDF") como un evento discreto sobre un conjunto completo, no una generación parcial -- descartada por no tener evidencia en el guión de eventos, mismo criterio que ya excluyó acciones en bloque no evidenciadas (ver [catálogo de actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md)). Nota aparte, ya apuntada en la discussion [#33](https://github.com/mmasias/pyCelda/discussions/33): esto valida solo el **estado** (`Aprobada`), no la **completitud de contenido** (profesorado/RA/MD/`SistemaEvaluacion` ponderados) -- sigue fuera de alcance.

Postcondición: `fechaGeneracionPDF` se actualiza en cada `Guia` del `Programa` generada -- mismo atributo que [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md) consulta para decidir si ofrece el botón de descarga.

**Temario en el PDF**: cada PDF renderiza `Guia.contenido` (el temario propio de esa guía concreta, redactado por el profesor cada curso), **no** `Guia.asignaturaPrograma.contenido` (referencia estructural del programa) -- discussion [#191](https://github.com/mmasias/pyCelda/discussions/191). Antes del retroceso de #191 la `Guia` no materializaba contenido y lo heredaba de `AsignaturaPrograma` al renderizar; ahora lo lleva propio.

**Requisitos previos en el PDF (discussion [#259](https://github.com/mmasias/pyCelda/discussions/259))**: la sección 2 renderiza `AsignaturaPrograma.requisitosPrevios` (atributo de texto plano nuevo) leído **en vivo**, no materializado en la `Guia` -- sustituye el literal `_REQUISITOS_PREVIOS_AQUI_`. Consecuencia: dos PDF generados en la misma tanda para guías de la misma `AsignaturaPrograma` comparten el texto de requisitos previos, aunque su `Guia.contenido` difiera. La deuda de congelar el valor al aprobar es común con los RA y se resuelve en [#219](https://github.com/mmasias/pyCelda/issues/219).

Datos del wireframe: pantalla **bloqueada** con dato real, sin hipótesis -- `GII__IYA003` realmente `Borrador`, motivo real del bloqueo. Pantalla **generada** con la misma `Guia` mostrada hipotéticamente `Aprobada` (necesaria para ilustrar el camino de éxito, documentado igual que el resto del lote en la discussion #44).

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SISTEMA_DISPONIBLE --> SISTEMA_DISPONIBLE : generarGuiasPDF()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catálogo de casos de uso de `Admin` sobre `Guia`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) -- guión de eventos, `fechaGeneracionPDF`
- [`notificarGuiasActualizadas()`](../notificarGuiasActualizadas/README.md) -- aviso del `DirectorPrograma` que dispara este caso de uso
- [Discussion #33](https://github.com/mmasias/pyCelda/discussions/33) -- validación de completitud de contenido, fuera de alcance
- [Discussion #44](https://github.com/mmasias/pyCelda/discussions/44) -- cierre de L9, punto 3
- [Discussion #191](https://github.com/mmasias/pyCelda/discussions/191) -- el PDF renderiza `Guia.contenido` propio, no el heredado de `AsignaturaPrograma`
- [Discussion #259](https://github.com/mmasias/pyCelda/discussions/259) -- `AsignaturaPrograma.requisitosPrevios` (texto plano en vivo) en la sección 2 del PDF (ítem 2 de #217)
