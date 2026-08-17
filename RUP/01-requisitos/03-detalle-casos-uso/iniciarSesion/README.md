<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > iniciarSesion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/iniciarSesion/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`UsuarioNoLogueado`|
|**Objetivo**|Validar credenciales y, según el rol que resulte identificado, ceder el punto de extensión correspondiente|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

**El invocador es `UsuarioNoLogueado`, no `Profesor`/`DirectorGrado`/`Admin`.** Un rol específico solo existe *después* de validar credenciales con éxito -- no puede ser quien invoca la propia validación, porque en el momento de la invocación el sistema aún no sabe cuál de los tres es. Simétricamente, `cerrarSesion()` (antes sin modelar en ningún `actoresCasosUso*.puml`) sí la invoca el rol ya identificado: `Profesor -- cerrarSesion()` (heredado por `DirectorGrado`), `Admin -- cerrarSesion()` declarado aparte.

## Tres destinos, uno por rol

Un único punto de extensión ("tras validación exitosa"), tres ramas mutuamente excluyentes según el rol que resulte identificado:

<div align=center>

|`Profesor`|`DirectorGrado`|`Admin`|
|:-:|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturasGrado/wireframe-porProfesor.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirGrados/wireframe-porDirector.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirPanelAdministracion/wireframe.svg)|
|<sup>`abrirAsignaturasGrado()` extiende</sup>|<sup>`abrirGrados()` extiende</sup>|<sup>`abrirPanelAdministracion()` extiende</sup>|

</div>

Ninguno de los tres tiene wireframe propio en esta ficha: la pantalla de cada rama es la de un CU ya catalogado que **extiende** a `iniciarSesion()` con una condición (`rol == Profesor` / `rol == DirectorGrado` / `rol == Admin`), no contenido nuevo -- simetría completa entre los tres roles, sin excepción para `Admin`. Esta carpeta no tiene `wireframes.puml` propio.

**`<<extend>>`, no `<<include>>`.** `<<include>>` es incondicional por definición UML: el caso base *siempre* incorpora el incluido, sin ramificación -- pensado para comportamiento común factorizado. Aquí solo se dispara *una* de tres ramas según una condición evaluada en tiempo de ejecución (qué rol resultó identificado), y `iniciarSesion()` es completo y tiene sentido sin ninguna extensión -- exactamente la semántica de `<<extend>>`: opcional, condicional, insertado en un punto de extensión nombrado del caso base. La dirección de la flecha también se invierte respecto a `<<include>>`: va del caso que extiende al caso base (`abrirAsignaturasGrado ..> iniciarSesion : <<extend>>`), no al revés.

**Fracaso de credenciales**: self-loop sobre `SESION_CERRADA`, sin transición de estado -- detectado originalmente al construir la especificación de `enviarGuiaARevision()`, documentado como comentario en `diagramaContextoProfesor.puml` antes de que esta ficha existiera.

## Historial de correcciones

- **Origen (issue [#49](https://github.com/mmasias/pyCelda/issues/49))**: el issue [#42](https://github.com/mmasias/pyCelda/issues/42) (cerrado) concluyó que `Profesor` no necesita un CU de navegación separado del login. Sigue siendo correcto -- `diagramaContextoProfesor.puml` no cambia. Lo que faltaba era la relación formal: sin ficha de catálogo, resuelto en el mockup con un override que reutilizaba el wireframe de `DirectorGrado` sin que el catálogo lo reflejara.
- **Replicado para `DirectorGrado` (issue [#50](https://github.com/mmasias/pyCelda/issues/50))**: mismo mecanismo de credenciales, destino propio.
- **Corrección de actor**: las tres versiones anteriores asociaban `iniciarSesion()` directamente al rol específico (`Profesor -- iniciarSesion`, etc.) -- error sistemático de la bibliografía RUP. Corregido a `UsuarioNoLogueado`.
- **Corrección de relación**: las tres versiones anteriores modelaban `abrirAsignaturasGrado()`/`abrirGrados()` como `<<include>>` de `iniciarSesion()`. Incondicional por definición, no encajaba con una relación disparada por una de tres condiciones mutuamente excluyentes. Corregido a `<<extend>>`, flecha invertida, con condición y punto de extensión nombrados.
- **`Admin` (issue [#51](https://github.com/mmasias/pyCelda/issues/51)), primer cierre y su corrección**: modelado originalmente como contenido propio de `iniciarSesion()`, sin CU independiente -- sin motivo de reutilización cruzada entre actores, a diferencia de `abrirAsignaturasGrado()`/`abrirGrados()`. Ese cierre no consideraba las vueltas desde cada área de catálogo de `Admin` hacia `SISTEMA_DISPONIBLE` (`diagramaContextoAdmin.puml`), modeladas como `completarGestion()` genérico sin destino nombrable -- `iniciarSesion()` no podía serlo, su actor es `UsuarioNoLogueado`, no invocable a mitad de sesión. Corregido creando [`abrirPanelAdministracion()`](../abrirPanelAdministracion/README.md), simétrico a los otros dos roles, al cerrar el patrón completo de `completarGestion()` en los tres diagramas de contexto (discussion [#47](https://github.com/mmasias/pyCelda/discussions/47)).

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `SESION_CERRADA --> ASIGNATURAS_GRADO_ABIERTO : iniciarSesion()`, self-loop de fracaso
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `SESION_CERRADA --> GRADOS_ABIERTO : iniciarSesion()`, destino propio
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SESION_CERRADA --> SISTEMA_DISPONIBLE : iniciarSesion()`
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) / [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) / [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- relación `<<extend>>` con condición, una por actor
- [`abrirAsignaturasGrado()`](../abrirAsignaturasGrado/README.md) -- extiende para `Profesor`, con su variante filtrada
- [`abrirGrados()`](../abrirGrados/README.md) -- extiende para `DirectorGrado`, con su variante filtrada
- [`abrirPanelAdministracion()`](../abrirPanelAdministracion/README.md) -- extiende para `Admin`, sin variante (actor único)
- Issue [#42](https://github.com/mmasias/pyCelda/issues/42) / [#48](https://github.com/mmasias/pyCelda/issues/48) / [#49](https://github.com/mmasias/pyCelda/issues/49) / [#50](https://github.com/mmasias/pyCelda/issues/50) / [#51](https://github.com/mmasias/pyCelda/issues/51) -- huecos originales cerrados
- Discussion [#47](https://github.com/mmasias/pyCelda/discussions/47) -- planificación de Análisis, origen de esta ficha y de la corrección de `Admin`
