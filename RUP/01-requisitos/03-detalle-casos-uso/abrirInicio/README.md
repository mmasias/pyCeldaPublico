<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirInicio()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirInicio/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirInicio/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor` / `DirectorGrado`|
|**Objetivo**|Aterrizar tras iniciar sesión en una única pantalla que reúne los dos listados que la cuenta puede tener a su cargo: sus guías (como `Profesor`) y sus grados (como `DirectorGrado`)|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

**Primitiva de navegación, no cuenta en el catálogo de 103 casos de uso** -- misma categoría que [`iniciarSesion()`](../iniciarSesion/README.md)/`cerrarSesion()`/[`abrirPanelAdministracion()`](../abrirPanelAdministracion/README.md), distinta de [`abrirAsignaturasGrado()`](../abrirAsignaturasGrado/README.md)/[`abrirGrados()`](../abrirGrados/README.md) (que sí cuentan: listan entidades reales del dominio). `abrirInicio()` no lista nada propio: **compone** esos dos casos de uso ya catalogados (`<<include>>`), sin `<<choice>>`, sin lectura de dominio nueva y sin postcondición sobre ninguna entidad. Tener ficha completa (especificación, wireframe, README) no es indicio de que cuente -- `iniciarSesion()`/`abrirPanelAdministracion()` ya establecen ese precedente.

Es el destino que [`iniciarSesion()`](../iniciarSesion/README.md) extiende cuando el rol identificado es `Profesor` o `DirectorGrado` (condición `rol in {Profesor, DirectorGrado}`, punto de extensión "tras validación exitosa"). La rama de `Admin` sigue extendiendo a [`abrirPanelAdministracion()`](../abrirPanelAdministracion/README.md), sin cambio.

## Dos secciones, según lo que la cuenta tenga a su cargo

<div align=center>

|Sección|Se muestra cuando|Contenido|
|-|-|-|
|**Mis guías**|la cuenta tiene fila en `Profesor`|el listado de [`abrirAsignaturasGrado()`](../abrirAsignaturasGrado/README.md) en su variante filtrada por profesor (`wireframe-porProfesor`), embebido -- con la cardinalidad actual (1 `AsignaturaGrado` : 1 `Guia`) es de hecho la lista de sus guías|
|**Mis grados**|la cuenta dirige `>= 1` `Grado`|el listado de [`abrirGrados()`](../abrirGrados/README.md) en su variante filtrada por director (`wireframe-porDirector`), embebido|

</div>

Los dos casos de uso embebidos ya extendían directamente a `iniciarSesion()` -- uno por rol, ramas mutuamente excluyentes. Ahora `iniciarSesion()` extiende a `abrirInicio()`, y `abrirInicio()` los `<<include>>` a los dos. La cuenta con doble identidad (`DirectorGrado` **y** `Profesor`, roles independientes no exclusivos en el modelo de dominio) ve **las dos secciones a la vez** -- caso que antes exigía un tercer punto de extensión propio de `abrirAsignaturasGrado()` ([issue #103](https://github.com/mmasias/pyCelda/issues/103), 2026-08-22), ahora **subsumido**: el hub es las dos listas juntas por construcción.

**Enlace "Manual del profesor" (issue [#321](https://github.com/mmasias/pyCelda/issues/321))**: dentro de la sección "Mis guías", un enlace externo real al manual de usuario del `Profesor` ([#318](https://github.com/mmasias/pyCelda/issues/318)), publicado en `pyCeldaPublico` (repo público, el privado no serviría a una cuenta real sin acceso), abierto en pestaña nueva. No es CU nuevo -- es una ayuda de navegación externa, sin lectura de dominio ni `<<choice>>`, igual criterio que el resto de retoques de este hub. Primer enlace externo real de la aplicación: a diferencia del `mailto:` descartado en [#312](https://github.com/mmasias/pyCelda/issues/312) (decorar un dato interno como navegación, sin destino real fuera de la app), aquí el destino sí es genuinamente externo, así que un enlace normal es el mecanismo correcto.

**Una capacidad ausente se presenta como sección vacía, nunca como error.** Un `Profesor` que no dirige ningún `Grado` ve "Mis grados" sin filas (o directamente sin la sección); un ex-director que ya no dirige nada -- fila huérfana en `directores_grado` que `quitarDirectorGrado()` nunca borra -- entra igual (su rol se resuelve como `Profesor`, ver [`iniciarSesion()`](../iniciarSesion/README.md)) y aterriza aquí, no en un `/grados` vacío sin salida. Nunca se expulsa a una cuenta autenticada y reconocida por el catálogo.

## Origen

Cierre de diseño en la [discussion #274](https://github.com/mmasias/pyCelda/discussions/274) (Opción C). El hecho que lo motiva: `get_current_rol()` resolvía `director_grado` para cualquier email con fila en `directores_grado`, con o sin grados a su cargo, y ese rol enrutaba a `/grados`; un `Profesor` que además fuese (ex-)director quedaba enrutado de forma permanente a un listado de grados vacío, con un clic extra para llegar a sus guías. Afecta a todo ex-director docente, no solo a la beta de profesores. La Opción C sustituye la elección de una sola pantalla por rol por una pantalla de inicio única que compone ambos listados.

## Referencias

- [Especificación de Requisitos](especificacion.puml) y [wireframes](wireframes.puml) -- fuente de verdad de la composición de dos secciones.
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) / [DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `SESION_CERRADA --> INICIO_ABIERTO : iniciarSesion()`, estado nuevo `INICIO_ABIERTO`.
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) / [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- `abrirInicio ..> iniciarSesion : <<extend>>`, `abrirInicio ..> {abrirAsignaturasGrado, abrirGrados} : <<include>>`.
- [`iniciarSesion()`](../iniciarSesion/README.md) -- caso base extendido; de tres ramas `<<extend>>` por rol a dos (`abrirInicio()` / `abrirPanelAdministracion()`).
- [`abrirAsignaturasGrado()`](../abrirAsignaturasGrado/README.md) / [`abrirGrados()`](../abrirGrados/README.md) -- casos incluidos; dejan de extender `iniciarSesion()` directamente.
- [`abrirPanelAdministracion()`](../abrirPanelAdministracion/README.md) -- primitiva de navegación análoga para `Admin`, mismo estatus de "ficha completa, fuera del catálogo".
- [Dashboard de seguimiento](/RUP/99-seguimiento/README.md) -- nota bajo la tabla de Estadísticas sobre por qué no suma al 103.
- Discussion [#274](https://github.com/mmasias/pyCelda/discussions/274) -- cierre de diseño (Opción C).
- Issue [#103](https://github.com/mmasias/pyCelda/issues/103) -- tercer punto de extensión de `abrirAsignaturasGrado()` (doble identidad), subsumido por este caso.
- Issue [#318](https://github.com/mmasias/pyCelda/issues/318) -- manual de usuario de `Profesor`. Issue [#321](https://github.com/mmasias/pyCelda/issues/321) -- enlace al manual desde esta pantalla.
