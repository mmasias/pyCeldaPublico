<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirPanelAdministracion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirPanelAdministracion/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirPanelAdministracion/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Volver al panel de administración (`SISTEMA_DISPONIBLE`), punto de partida de todo el catálogo de `Admin`|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

**Primitiva de navegación, no cuenta en el catálogo de 91 casos de uso** -- misma categoría que [`iniciarSesion()`](../iniciarSesion/README.md)/`cerrarSesion()`, distinta de [`abrirAsignaturasGrado()`](../abrirAsignaturasGrado/README.md)/[`abrirGrados()`](../abrirGrados/README.md) (que sí cuentan: listan entidades reales del dominio, `AsignaturaGrado`/`Grado`). El panel no tiene dato de dominio detrás -- es un menú fijo de seis enlaces (`Universidades`, `Asignaturas`, `MetodologiasDocentes`, `Profesores`, `CursosAcademicos`, más el propio `generarGuiasPDF()` como self-loop), sin `<<choice>>` ni postcondición sobre ninguna entidad. Tener ficha propia (especificación, wireframe, README) no es indicio de que cuente -- `iniciarSesion()` ya establece el precedente de una primitiva completamente documentada y aun así excluida.

Es el destino que `iniciarSesion()` extiende cuando el rol identificado es `Admin`, y al que vuelven las cinco áreas de catálogo tras completar su gestión. Sin parámetro, a diferencia de `abrirAsignaturasGrado()`/`abrirGrados()`: `Admin` es un único actor, sin variante filtrada que resolver.

**Corrige una decisión anterior, no una simplificación puntual.** El primer cierre de `iniciarSesion()` (issue [#51](https://github.com/mmasias/pyCelda/issues/51)) modeló el panel como contenido propio de `iniciarSesion()`, sin CU independiente. Ese cierre no consideraba las cinco vueltas desde cada área de catálogo hacia `SISTEMA_DISPONIBLE`, modeladas como `completarGestion()` genérico en `diagramaContextoAdmin.puml` -- y `completarGestion()` no es una acción con identidad propia, es un placeholder de "vuelve al punto de partida" que se resuelve al nombre real en cuanto ese destino tiene uno (mismo criterio, aplicado ya a `Profesor`/`DirectorGrado`, que no dejan ningún `completarGestion()` sin resolver). `iniciarSesion()`, además, no puede ser ese nombre: su actor es `UsuarioNoLogueado`, no invocable por un `Admin` ya autenticado a mitad de sesión. Sin un CU propio con actor `Admin`, esas cinco vueltas no tenían destino nombrable -- hueco real, no una preferencia de estilo. Corregido junto con el resto del catálogo de `completarGestion()` (discussion [#47](https://github.com/mmasias/pyCelda/discussions/47), sesión de planificación de Análisis).

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `UNIVERSIDADES_ABIERTO`/`ASIGNATURAS_ABIERTO`/`METODOLOGIAS_DOCENTES_ABIERTO`/`PROFESORES_ABIERTO`/`CURSOS_ACADEMICOS_ABIERTO --> SISTEMA_DISPONIBLE : abrirPanelAdministracion()`
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- `Admin -- abrirPanelAdministracion`, `<<extend>>` de `iniciarSesion()`
- [`iniciarSesion()`](../iniciarSesion/README.md) -- extendido en el punto "tras validación exitosa", condición `rol == Admin`; mismo estatus de primitiva sin contar
- [`abrirAsignaturasGrado()`](../abrirAsignaturasGrado/README.md) / [`abrirGrados()`](../abrirGrados/README.md) -- mismo papel estructural para `Profesor`/`DirectorGrado`, pero sí cuentan (listan entidades reales)
- Discussion [#47](https://github.com/mmasias/pyCelda/discussions/47) -- planificación de Análisis, origen de la corrección
- Issue [#51](https://github.com/mmasias/pyCelda/issues/51) -- decisión original que esta ficha corrige
