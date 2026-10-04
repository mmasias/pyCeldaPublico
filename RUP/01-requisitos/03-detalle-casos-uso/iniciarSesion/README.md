<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/iniciarSesion/README.md) / [Diseño](/RUP/03-diseño/casos-uso/iniciarSesion/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > iniciarSesion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/iniciarSesion/README.md)|[Diseño](/RUP/03-diseño/casos-uso/iniciarSesion/README.md)|[Desarrollo](/RUP/04-desarrollo/casos-uso/iniciarSesion/README.md)|Pruebas|
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

**El invocador es `UsuarioNoLogueado`, no `Profesor`/`DirectorPrograma`/`Admin`.** Un rol específico solo existe *después* de validar credenciales con éxito -- no puede ser quien invoca la propia validación, porque en el momento de la invocación el sistema aún no sabe cuál de los tres es. Simétricamente, `cerrarSesion()` (antes sin modelar en ningún `actoresCasosUso*.puml`) sí la invoca el rol ya identificado: `Profesor -- cerrarSesion()` (heredado por `DirectorPrograma`), `Admin -- cerrarSesion()` declarado aparte.

## Dos destinos tras validar

Un único punto de extensión ("tras validación exitosa"), **dos** ramas mutuamente excluyentes según el rol que resulte identificado:

<div align=center>

|`Profesor` / `DirectorPrograma`|`Admin`|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirInicio/wireframe.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirPanelAdministracion/wireframe.svg)|
|<sup>[`abrirInicio()`](../abrirInicio/README.md) extiende (cond. `rol in {Profesor, DirectorPrograma}`)</sup>|<sup>[`abrirPanelAdministracion()`](../abrirPanelAdministracion/README.md) extiende (cond. `rol == Admin`)</sup>|

</div>

Ninguna de las dos tiene wireframe propio en esta ficha: la pantalla de cada rama es la de una primitiva de navegación ya catalogada que **extiende** a `iniciarSesion()` con una condición, no contenido nuevo. Esta carpeta no tiene `wireframes.puml` propio.

**De tres ramas a dos (discussion [#274](https://github.com/mmasias/pyCelda/discussions/274)).** Antes había tres ramas simétricas: `Profesor -> abrirAsignaturasPrograma()`, `DirectorPrograma -> abrirProgramas()`, `Admin -> abrirPanelAdministracion()`. Un email con doble identidad (`DirectorPrograma` **y** `Profesor`, roles no exclusivos) quedaba enrutado a una sola de ellas -- en la práctica, `abrirProgramas()`, que para un ex-director sin programas a su cargo es un listado vacío sin salida directa a sus guías. La rama de `Profesor` y la de `DirectorPrograma` se fusionan en [`abrirInicio()`](../abrirInicio/README.md), que compone "Mis guías" y "Mis programas" en una pantalla; la de `Admin` no cambia.

**Nunca se expulsa a una cuenta autenticada y reconocida por el catálogo.** El `<<choice>>` de "validación exitosa" resuelve el rol contra `Profesor`/`DirectorPrograma`/`Admin`; una capacidad ausente (no impartir, no dirigir ningún `Programa`) se traduce en una sección vacía de `abrirInicio()`, no en un `403`. El caso concreto: un ex-director que ya no dirige nada -- fila huérfana en `directores_programa` que [`quitarDirectorPrograma()`](../quitarDirectorPrograma/README.md) nunca borra -- resuelve `rol == Profesor` (imparta o no) y aterriza en `abrirInicio()`. El `<<choice>>` **no** gana una rama nueva para ese caso degenerado (mínima superficie de mantenimiento).

**`<<extend>>`, no `<<include>>`.** `<<include>>` es incondicional por definición UML: el caso base *siempre* incorpora el incluido, sin ramificación -- pensado para comportamiento común factorizado. Aquí solo se dispara *una* de dos ramas según una condición evaluada en tiempo de ejecución (qué rol resultó identificado), y `iniciarSesion()` es completo y tiene sentido sin ninguna extensión -- exactamente la semántica de `<<extend>>`: opcional, condicional, insertado en un punto de extensión nombrado del caso base. La dirección de la flecha también se invierte respecto a `<<include>>`: va del caso que extiende al caso base (`abrirInicio ..> iniciarSesion : <<extend>>`), no al revés. (`abrirInicio()` sí `<<include>>` a `abrirAsignaturasPrograma()` y `abrirProgramas()` -- ahí la inclusión sí es incondicional: el hub incorpora las dos secciones siempre, y la vacuidad por rol es un resultado de datos, no una rama.)

**Fracaso de credenciales**: self-loop sobre `SESION_CERRADA`, sin transición de estado -- detectado originalmente al construir la especificación de `enviarGuiaARevision()`, documentado como comentario en `diagramaContextoProfesor.puml` antes de que esta ficha existiera.

**Enlace "Manual del profesor" (issue [#326](https://github.com/mmasias/pyCelda/issues/326))**: en la propia pantalla de `SESION_CERRADA` (antes de validar credenciales), un enlace externo al manual de usuario del `Profesor` ([#318](https://github.com/mmasias/pyCelda/issues/318)), el mismo destino y mecanismo que el ya presente en `abrirInicio()` ([#321](https://github.com/mmasias/pyCelda/issues/321)) -- misma etiqueta "Manual del profesor" aunque la pantalla la vean tanto `Profesor` como `DirectorPrograma`. No es CU nuevo: ayuda de navegación externa, sin lectura de dominio ni `<<choice>>`.

**Enlace "Manual del director de programa" (issue [#336](https://github.com/mmasias/pyCelda/issues/336))**: una vez existió el manual de `DirectorPrograma` ([#329](https://github.com/mmasias/pyCelda/issues/329)) y su enlace equivalente en `abrirInicio()` ([#333](https://github.com/mmasias/pyCelda/issues/333)), se añade también aquí, junto al de Profesor -- los dos conviven en `SESION_CERRADA` igual que ya conviven en `INICIO_ABIERTO`/`abrirInicio()`, sin filtrar el rol de la cuenta (que todavía no se conoce en esta pantalla).

## Historial de correcciones

- **Origen (issue [#49](https://github.com/mmasias/pyCelda/issues/49))**: el issue [#42](https://github.com/mmasias/pyCelda/issues/42) (cerrado) concluyó que `Profesor` no necesita un CU de navegación separado del login. Sigue siendo correcto -- `diagramaContextoProfesor.puml` no cambia. Lo que faltaba era la relación formal: sin ficha de catálogo, resuelto en el mockup con un override que reutilizaba el wireframe de `DirectorPrograma` sin que el catálogo lo reflejara.
- **Replicado para `DirectorPrograma` (issue [#50](https://github.com/mmasias/pyCelda/issues/50))**: mismo mecanismo de credenciales, destino propio.
- **Corrección de actor**: las tres versiones anteriores asociaban `iniciarSesion()` directamente al rol específico (`Profesor -- iniciarSesion`, etc.) -- error sistemático de la bibliografía RUP. Corregido a `UsuarioNoLogueado`.
- **Corrección de relación**: las tres versiones anteriores modelaban `abrirAsignaturasPrograma()`/`abrirProgramas()` como `<<include>>` de `iniciarSesion()`. Incondicional por definición, no encajaba con una relación disparada por una de tres condiciones mutuamente excluyentes. Corregido a `<<extend>>`, flecha invertida, con condición y punto de extensión nombrados.
- **`Admin` (issue [#51](https://github.com/mmasias/pyCelda/issues/51)), primer cierre y su corrección**: modelado originalmente como contenido propio de `iniciarSesion()`, sin CU independiente -- sin motivo de reutilización cruzada entre actores, a diferencia de `abrirAsignaturasPrograma()`/`abrirProgramas()`. Ese cierre no consideraba las vueltas desde cada área de catálogo de `Admin` hacia `SISTEMA_DISPONIBLE` (`diagramaContextoAdmin.puml`), modeladas como `completarGestion()` genérico sin destino nombrable -- `iniciarSesion()` no podía serlo, su actor es `UsuarioNoLogueado`, no invocable a mitad de sesión. Corregido creando [`abrirPanelAdministracion()`](../abrirPanelAdministracion/README.md), simétrico a los otros dos roles, al cerrar el patrón completo de `completarGestion()` en los tres diagramas de contexto (discussion [#47](https://github.com/mmasias/pyCelda/discussions/47)).
- **Fusión de las ramas `Profesor`/`DirectorPrograma` en [`abrirInicio()`](../abrirInicio/README.md) (discussion [#274](https://github.com/mmasias/pyCelda/discussions/274))**: las dos ramas tenían destinos distintos (`abrirAsignaturasPrograma()` filtrada / `abrirProgramas()` filtrada) pero un email con doble identidad solo alcanzaba una. `get_current_rol()` priorizaba `DirectorPrograma` en cuanto había fila en `directores_programa`, con o sin programas a su cargo -- un ex-director docente quedaba enrutado de forma permanente a un listado de programas vacío. Se sustituyen las dos ramas por una sola hacia `abrirInicio()`, primitiva de navegación que compone ambos listados; el rol solo distingue ya `abrirInicio()` (Profesor/DirectorPrograma) de `abrirPanelAdministracion()` (Admin). Se añade el guard de resolución de rol: `director_programa` solo si el email dirige `>= 1` `Programa`; la fila huérfana cae a `profesor` sin llegar nunca a `403`.

## Notas de diseño y trazabilidad

- Modelado: invocado por `UsuarioNoLogueado`, no por Profesor/DirectorPrograma/Admin; el rol específico solo existe después de que `iniciarSesion()` tenga éxito, y quien invoca no puede ser el resultado de la propia invocación. Los actores ya identificados invocan `cerrarSesion()`, nunca `iniciarSesion()` (ver `actoresCasosUso{Profesor,DirectorPrograma,AdminCatalogos}.puml`).

- Punto de extensión "tras validación exitosa" (rama verde de `<<choice>>` c). Dos ramas mutuamente excluyentes según el rol resuelto (discussion [#274](https://github.com/mmasias/pyCelda/discussions/274), antes eran tres): rol in {Profesor, DirectorPrograma} -> `abrirInicio()` (primitiva de navegación que compone "Mis guías" y "Mis programas"); rol == Admin -> `abrirPanelAdministracion()`. Ambas extienden a `iniciarSesion()`, no lo incluyen: `<<include>>` es incondicional por definición UML, aquí solo se dispara una de dos ramas según el rol y `iniciarSesion()` es completo sin ninguna extensión (semántica de `<<extend>>`).

- Guard de resolución de rol (#274): el rol es `director_programa` solo si el email dirige >= 1 Programa; una fila huérfana en `directores_programa` (ex-director sin programas) cae a `profesor` y nunca a un fallo; la capacidad ausente se presenta como sección vacía de `abrirInicio()`.

- Regla de presentación de las pantallas de login (`Login.tsx` y `AdminLogin.tsx`, issues [#628](https://github.com/mmasias/pyCelda/issues/628) y [#630](https://github.com/mmasias/pyCelda/issues/630)): el pie muestra la versión de la aplicación seguida de la versión del esquema de la base de datos, "... - v<versión> · esquema N". La versión del esquema se consulta al sistema sin sesión, porque el login es previo a ella. Es un dato informativo: si la consulta falla, el sufijo " · esquema N" se omite sin mostrar error. No es un caso de uso propio, es presentación de `iniciarSesion()`.

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `SESION_CERRADA --> INICIO_ABIERTO : iniciarSesion()`, self-loop de fracaso
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `SESION_CERRADA --> INICIO_ABIERTO : iniciarSesion()`, mismo destino que Profesor
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SESION_CERRADA --> SISTEMA_DISPONIBLE : iniciarSesion()`
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) / [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) / [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- relación `<<extend>>` con condición: `abrirInicio()` para Profesor/DirectorPrograma, `abrirPanelAdministracion()` para Admin
- [`abrirInicio()`](../abrirInicio/README.md) -- primitiva que extiende para `Profesor`/`DirectorPrograma`; `<<include>>` de `abrirAsignaturasPrograma()` + `abrirProgramas()`
- [`abrirAsignaturasPrograma()`](../abrirAsignaturasPrograma/README.md) / [`abrirProgramas()`](../abrirProgramas/README.md) -- variantes filtradas incluidas por `abrirInicio()`; ya no extienden `iniciarSesion()` directamente
- [`abrirPanelAdministracion()`](../abrirPanelAdministracion/README.md) -- extiende para `Admin`, sin variante (actor único)
- Issue [#42](https://github.com/mmasias/pyCelda/issues/42) / [#48](https://github.com/mmasias/pyCelda/issues/48) / [#49](https://github.com/mmasias/pyCelda/issues/49) / [#50](https://github.com/mmasias/pyCelda/issues/50) / [#51](https://github.com/mmasias/pyCelda/issues/51) -- huecos originales cerrados
- Discussion [#47](https://github.com/mmasias/pyCelda/discussions/47) -- planificación de Análisis, origen de esta ficha y de la corrección de `Admin`
- Issue [#318](https://github.com/mmasias/pyCelda/issues/318) -- manual de usuario de `Profesor`. Issue [#321](https://github.com/mmasias/pyCelda/issues/321) -- enlace en `abrirInicio()`. Issue [#326](https://github.com/mmasias/pyCelda/issues/326) -- mismo enlace aquí, en `SESION_CERRADA`
- Issue [#329](https://github.com/mmasias/pyCelda/issues/329) -- manual de usuario de `DirectorPrograma`. Issue [#333](https://github.com/mmasias/pyCelda/issues/333) -- enlace en `abrirInicio()`. Issue [#336](https://github.com/mmasias/pyCelda/issues/336) -- mismo enlace aquí, en `SESION_CERRADA`
