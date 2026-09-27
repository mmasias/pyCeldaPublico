<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > abrirInicio()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirInicio/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirInicio/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirInicio()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirInicio/README.md): primitiva de navegación que compone dos casos de uso ya catalogados, sin `<<choice>>` ni dato de dominio propio. Mismo estatus que [`abrirPanelAdministracion()`](../abrirPanelAdministracion/README.md): no cuenta en el catálogo de 102, pero tiene ficha completa.

**Sin `Controlador` ni `Modelo` propios**: `abrirInicio()` no recupera ni muta ningún dato por su cuenta -- cada sección la resuelve el caso de uso que incluye, con su propio controlador y repositorio ya cerrados en Análisis (`AbrirAsignaturasGradoView`/`GradoController` para "Mis guías", `AbrirGradosView`/`GradoController` para "Mis grados"). La `Vista` de `abrirInicio()` solo compone esas dos y ofrece la navegación a abrir una guía o un grado concretos.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirInicio/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirInicioView`

**Responsabilidades:**
- compone la sección "Mis guías" (`<<include>>` de [`abrirAsignaturasGrado()`](../abrirAsignaturasGrado/README.md) en su variante filtrada por profesor) si la cuenta tiene fila en `Profesor`.
- compone la sección "Mis grados" (`<<include>>` de [`abrirGrados()`](../abrirGrados/README.md) en su variante filtrada por director) si la cuenta dirige `>= 1` `Grado`.
- una sección cuya capacidad no aplica se presenta vacía o ausente, nunca como error -- el punto de entrada tras el login no puede fallar para una cuenta ya autenticada y reconocida.
- ofrece la navegación a `abrirGuia()` (desde una fila de "Mis guías") y a `abrirGrado()` (desde una fila de "Mis grados").

**Colaboraciones:**
- **Entrada:** `:SESION_CERRADA` -- alcanzable como `<<extend>>` de [`iniciarSesion()`](../iniciarSesion/README.md) (condición `rol in {Profesor, DirectorGrado}`, punto "tras validación exitosa"). La rama de `Admin` extiende a [`abrirPanelAdministracion()`](../abrirPanelAdministracion/README.md), no aquí.
- **Control:** ninguno propio -- cada sección usa el `GradoController` ya introducido por los casos incluidos.
- **Salida:** `:Collaboration AbrirAsignaturasGrado` / `:Collaboration AbrirGrados` (secciones incluidas), `:GUIA_ABIERTO` (`abrirGuia()`) o `:GRADO_ABIERTO` (`abrirGrado()`).

## Nota sobre la resolución de rol

El rol que decide qué extiende `iniciarSesion()` (`abrirInicio()` vs. `abrirPanelAdministracion()`) y qué secciones pinta `abrirInicio()` se resuelve en `SesionController.resolverRol(email)` (ver [Análisis de `iniciarSesion()`](../iniciarSesion/README.md)). Dos señales independientes que este caso consume:

- `esProfesor` -- fila en `Profesor`; pinta "Mis guías".
- `dirigeGrados` -- el email dirige `>= 1` `Grado` (fila en `DirectorGrado` **y** colección `directores` no vacía en algún `Grado`); pinta "Mis grados".

Un email con fila huérfana en `DirectorGrado` y cero grados a su cargo (ex-director, tras [`quitarDirectorGrado()`](../quitarDirectorGrado/README.md)) resuelve `rol == Profesor` si además imparte, y aun sin impartir nunca cae a un `403` -- entra al hub con ambas secciones vacías. El `<<choice>>` de `iniciarSesion()` **no** gana una rama nueva para este caso degenerado (decisión de mínima superficie de mantenimiento, discussion #274).

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirInicio/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirInicio/wireframes.puml) -- fuente de verdad de la composición.
- [`iniciarSesion()`](../iniciarSesion/README.md) -- caso base extendido; `SesionController.resolverRol()`.
- [`abrirAsignaturasGrado()`](../abrirAsignaturasGrado/README.md) / [`abrirGrados()`](../abrirGrados/README.md) -- casos incluidos, con su `Controlador`/`Repository` ya cerrados.
- [`abrirPanelAdministracion()`](../abrirPanelAdministracion/README.md) -- primitiva de navegación análoga para `Admin`.
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) / [DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- estado `INICIO_ABIERTO`.
- Discussion [#274](https://github.com/mmasias/pyCelda/discussions/274) -- cierre de diseño (Opción C).
