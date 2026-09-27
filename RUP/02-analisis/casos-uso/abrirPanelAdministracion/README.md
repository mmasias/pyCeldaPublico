<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > abrirPanelAdministracion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirPanelAdministracion/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirPanelAdministracion/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirPanelAdministracion()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirPanelAdministracion/README.md): primitiva de navegación pura, sin `<<choice>>` ni dato de dominio detrás -- un menú fijo de seis enlaces (`Universidades`, `Asignaturas`, `Metodologías docentes`, `Profesores`, `Cursos académicos`, más `generarGuiasPDF()` como self-loop). Mismo estatus que [`iniciarSesion()`](../iniciarSesion/README.md): no cuenta en el catálogo de 91 casos de uso, pero tiene ficha completa.

**Sin `Controlador` ni `Modelo`**: a diferencia de todos los demás CU ya traducidos, este no recupera ni muta ningún dato -- el contenido es estático (seis botones fijos), así que no hay nada que un controlador orqueste ni una clase de modelo que porte. La `Vista` navega directamente a los seis casos de uso ya catalogados.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirPanelAdministracion/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirPanelAdministracionView`

**Responsabilidades:**
- presenta el menú fijo de seis accesos: `Universidades`, `Asignaturas`, `Metodologías docentes`, `Profesores`, `Cursos académicos`, `Generar guías PDF` -- contenido estático, sin datos de dominio que cargar.

**Colaboraciones:**
- **Entrada:** `:SISTEMA_DISPONIBLE` -- el `Admin` solicita volver al panel; también alcanzable como `<<extend>>` de [`iniciarSesion()`](../iniciarSesion/README.md) (condición `rol == Admin`).
- **Control:** ninguno -- sin `<<choice>>` ni dato que recuperar.
- **Salida:** `:UNIVERSIDADES_ABIERTO` / `:ASIGNATURAS_ABIERTO` / `:METODOLOGIAS_DOCENTES_ABIERTO` / `:PROFESORES_ABIERTO` / `:CURSOS_ACADEMICOS_ABIERTO` (uno de los cinco, según el enlace elegido) o `:SISTEMA_DISPONIBLE` (self-loop de `generarGuiasPDF()`).

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirPanelAdministracion/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirPanelAdministracion/wireframes.puml) -- fuente de verdad del menú fijo.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `UNIVERSIDADES_ABIERTO`/`ASIGNATURAS_ABIERTO`/`METODOLOGIAS_DOCENTES_ABIERTO`/`PROFESORES_ABIERTO`/`CURSOS_ACADEMICOS_ABIERTO --> SISTEMA_DISPONIBLE : abrirPanelAdministracion()`.
- [`iniciarSesion()`](../iniciarSesion/README.md) -- extendido en el punto "tras validación exitosa", condición `rol == Admin`; mismo estatus de primitiva sin contar en el catálogo de 91.
- [`abrirUniversidades()`](../abrirUniversidades/README.md) -- primer eslabón del catálogo alcanzado desde este menú.
- Discussion [#47](https://github.com/mmasias/pyCelda/discussions/47) -- planificación de Análisis, origen de esta ficha en Requisitos.
- Discussion [#113](https://github.com/mmasias/pyCelda/discussions/113) -- encargo de este Análisis, bloque "Admin bottom-up".
