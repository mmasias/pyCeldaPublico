<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/quitarDirectorPrograma/README.md) / [Diseño](/RUP/03-diseño/casos-uso/quitarDirectorPrograma/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > quitarDirectorPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/quitarDirectorPrograma/README.md)|[Diseño](/RUP/03-diseño/casos-uso/quitarDirectorPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/quitarDirectorPrograma/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Bloqueada (único DirectorPrograma del Programa)|Confirmación (queda otro DirectorPrograma)|Desde el Programa (issue #492)|
|:-:|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/quitarDirectorPrograma/wireframe-bloqueada.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/quitarDirectorPrograma/wireframe-confirmacion.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/quitarDirectorPrograma/wireframe-desdePrograma.svg)|
|||<sup>Código fuente: [wireframes.puml](wireframes.puml)</sup>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Quitar el rol `DirectorPrograma` a un `Profesor` sobre un `Programa` concreto, siempre que quede al menos otro director|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

**Mismo patrón `<<choice>>` bloqueante que `eliminarFacultad()`/`eliminarProfesor()`**, aplicado a quitar un rol en vez de a borrar una entidad: un `Programa` no puede quedarse sin ningún `DirectorPrograma`, así que el `<<choice>>` valida al inicio, antes de presentar la pantalla de confirmación -- si el `Profesor` es el único director de ese `Programa`, el sistema bloquea sin llegar a preguntar "¿seguro?". Decisión cerrada en la discussion [#18](https://github.com/mmasias/pyCelda/discussions/18).

**Segunda entrada desde `PROGRAMA_ABIERTO`, issue [#492](https://github.com/mmasias/pyCelda/issues/492)**: **flujo alternativo del mismo caso de uso**, no uno nuevo -- mismo objetivo de actor, misma regla de negocio del 409 (único director), mismo endpoint `DELETE /profesores/{profesor_id}/directores-programa/{programa_id}` (resolviendo antes `DirectorPrograma.email -> Profesor.email` para obtener el `profesor_id` que la ruta exige, nunca `DirectorPrograma.id`). **Asimetría real frente a la entrada desde el Profesor, documentada tal cual está implementada**: `ProgramaAdmin.tsx` no tiene pantalla de confirmación propia -- el botón `[Quitar]` actúa directamente por fila, y el bloqueo por único director llega como mensaje de error tras el intento (mismo patrón que ya usa `DefinirDirectorPrograma.tsx` para sus propios errores de envío), no como una pantalla de aviso previa. La especificación refleja esta asimetría con dos ramas internas distintas por entrada en vez de forzar una simetría que el código no tiene.

## Notas de diseño y trazabilidad

- La segunda entrada ("Quitar" por fila desde `abrirPrograma()`) no tiene pantalla de confirmación propia: actúa directamente por fila (issue [#492](https://github.com/mmasias/pyCelda/issues/492)). La entrada desde el Profesor sí pide el paso "¿seguro?"; de ahí la asimetría reflejada en la especificación.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROFESOR_ABIERTO --> PROFESOR_ABIERTO : quitarDirectorPrograma()`, y ahora también `PROGRAMA_ABIERTO --> PROGRAMA_ABIERTO : quitarDirectorPrograma()` (issue #492)
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` sobre `Profesor` (sin cambio: flujo alternativo, no entrada nueva de catálogo)
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa o- DirectorPrograma` (agregación, muchos a muchos)
- [Discussion #18](https://github.com/mmasias/pyCelda/discussions/18) -- cierre del `<<choice>>` bloqueante
- [`definirDirectorPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/definirDirectorPrograma/README.md) -- caso de uso complementario (alta del rol), misma segunda entrada
- [`abrirPrograma()`](../abrirPrograma/README.md) -- portada donde vive la sección "Directores" que hospeda esta segunda entrada
- [Issue #492](https://github.com/mmasias/pyCelda/issues/492) -- origen de la segunda entrada y de la asimetría sin confirmación
