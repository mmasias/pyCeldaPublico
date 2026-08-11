<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirReferenciasBibliograficas()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirReferenciasBibliograficas/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirReferenciasBibliograficas/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor`|
|**Objetivo**|Consultar el listado de `ReferenciaBibliografica` de una `Guia`|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

Caso de uso reutilizado por `DirectorGrado`, misma ficha -- ver modelo del dominio (`DirectorGrado --|> Profesor`).

**Dos entradas, un solo retorno**, mismo patrón que [`abrirPonderacionesEvaluacion()`](../abrirPonderacionesEvaluacion/README.md): desde `GUIA_ABIERTO` y desde `REFERENCIA_BIBLIOGRAFICA_ABIERTO` (vuelta desde el detalle, mismo verbo plural reutilizado). La salida hacia `GUIA_ABIERTO` reutiliza [`abrirGuia()`](../abrirGuia/README.md).

Diez referencias reales de `GII__IYA003`, aportadas por el usuario en la discussion [#39](https://github.com/mmasias/pyCelda/discussions/39) (no estaban en el seed, a diferencia de `PonderacionEvaluacion`): dos `Basica`, tres `Complementaria`, cuatro `WebsReferencia`, una `OtrasFuentes` -- confirma que el enum de cuatro categorías del modelo de dominio cierra bien con el corpus real, incluida la nomenclatura exacta de la cuarta sección ("OTRAS FUENTES DE CONSULTA" en la guía real). `referencia` se muestra tal cual la aportó el usuario, sin normalizar (ISBN ausente, año dentro o fuera de la referencia, URL directa según el caso) -- mismo criterio documentado en el modelo del dominio.

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `GUIA_ABIERTO --> REFERENCIAS_BIBLIOGRAFICAS_ABIERTO : abrirReferenciasBibliograficas()`, `REFERENCIA_BIBLIOGRAFICA_ABIERTO --> REFERENCIAS_BIBLIOGRAFICAS_ABIERTO : abrirReferenciasBibliograficas()`
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catálogo de casos de uso de `Profesor` sobre `ReferenciaBibliografica`
- Modelo del dominio -- `Guia *-- ReferenciaBibliografica`, `tipo` enum cerrado de 4 valores
- [Discussion #39](https://github.com/mmasias/pyCelda/discussions/39) -- origen de los datos reales usados en este wireframe
