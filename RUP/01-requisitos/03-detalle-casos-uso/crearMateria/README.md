<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/crearMateria/README.md) / [Diseño](/RUP/03-diseño/casos-uso/crearMateria/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/crearMateria/README.md)|[Diseño](/RUP/03-diseño/casos-uso/crearMateria/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearMateria/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearMateria/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Dar de alta una `Materia` en un `Programa`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

**Módulo (issue [#762](https://github.com/mmasias/pyCelda/issues/762))**: el formulario gana un desplegable **Módulo** con los `Modulo` del `Programa` y la opción "Sin módulo" (por defecto). Es opcional (`Modulo o-- Materia`, 0..1) y solo ofrece módulos del mismo `Programa`; el servidor rechaza uno de otro programa (404). Los módulos se gestionan en [`abrirModulos()`](../abrirModulos/README.md).

**Actividades formativas (invariante de autopoblado, issue [#772](https://github.com/mmasias/pyCelda/issues/772))**: al crearse, la `Materia` recibe una fila a 0 horas y 0 % de presencialidad por cada `ActividadFormativa` del catálogo de su `Programa` ([`abrirActividadesFormativas()`](../abrirActividadesFormativas/README.md)). Es efecto del alta, sin paso adicional en el formulario: el reparto se edita después en [`editarActividadesFormativasMateria()`](../editarActividadesFormativasMateria/README.md). Un programa sin catálogo deja la materia sin filas. `codigoRuct` y `ects` de la `Materia` no se piden aquí: los escribe solo la importación desde el RUCT. Hasta #772 las filas venían del catálogo institucional de la `Universidad`.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `MATERIAS_ABIERTO --> MATERIA_ABIERTO : crearMateria()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catálogo de casos de uso de `Admin` sobre `Materia`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa *-- Materia`, `Materia{nombre}`; `caracter` vive en `AsignaturaPrograma`, no en `Materia` (una materia agrupa asignaturas de carácter distinto)
