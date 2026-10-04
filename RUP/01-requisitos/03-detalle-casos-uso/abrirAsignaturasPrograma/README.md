<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/abrirAsignaturasPrograma/README.md) / [Diseño](/RUP/03-diseño/casos-uso/abrirAsignaturasPrograma/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirAsignaturasPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/abrirAsignaturasPrograma/README.md)|[Diseño](/RUP/03-diseño/casos-uso/abrirAsignaturasPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturasPrograma/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturasPrograma/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorPrograma`, `Profesor`|
|**Objetivo**|Consultar el listado de `AsignaturaPrograma` de un `Programa`, con el profesorado que las imparte|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

Propio de `DirectorPrograma`, sin equivalente en `Admin`: el `Admin` no tiene un listado plural de `AsignaturaPrograma`, accede a ellas desde el atajo plano embebido en [`abrirPrograma()`](../abrirPrograma/README.md) (retocado en este mismo lote). El `DirectorPrograma`, en cambio, sí necesita ver de un vistazo todas las `AsignaturaPrograma` de su `Programa` junto con el profesorado asignado (`AsignaturaPrograma -- Profesor`, plantilla estable de impartición) -- de ahí el listado propio.

Columna **Profesorado**: dato ya presente en el modelo de dominio, mostrado en modo solo lectura -- la gestión de esa asignación (`asignarProfesorAAsignaturaPrograma()`/`desasignarProfesorAsignaturaPrograma()`, `Admin`) es de L6, todavía sin construir; no lleva botón propio en este listado.

Sin botón "Crear": `crearAsignaturaPrograma()` es exclusivo de `Admin`, no de `DirectorPrograma` (ver [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml)), mismo criterio que `abrirMaterias()` (`DirectorPrograma` la reutiliza para navegar, pero `crearMateria()` sigue siendo de `Admin`).

**Retocado al planificar Análisis (discussion #47)**: columna `Estado` añadida, con las cuatro `Guia.estado` posibles representadas -- necesario para el caso de uso piloto de Análisis (Profesor viendo sus guías en sus distintos estados). Tres filas nuevas, todas datos reales verificados contra `backend/app/data/seed/raw.json` (curso académico 2026-2027, GII), no fabricadas por adivinanza -- mismo criterio que la fila original: `Estructuras de datos y algoritmos I` (`IYA025`, curso 2, Dr. Manuel Masías Vergara) y `Ingeniería de Software I` (`IYA038`, curso 3, Dr. Manuel Masías Vergara) coinciden en profesorado con la fila original; `Redes de Ordenadores` (`IYA022`, curso 2) es del Dr. Mariano Benito Hoz, profesor distinto -- verificado, no asumido por continuidad con las demás filas.

**Caso de uso parametrizado (issue #48)**: la fila con profesorado mezclado (`Dr. Manuel Masías` en tres filas, `Dr. Mariano Benito Hoz` en la cuarta) es exactamente correcta para `DirectorPrograma`, que necesita ver todo el programa -- pero es la vista equivocada si se reutiliza sin más para `Profesor`, que solo debe ver sus propias `AsignaturaPrograma`. De ahí la segunda variante, `wireframe-porProfesor.svg`: mismo caso de uso, invocado con un parámetro (el profesor que consulta) en vez de sin filtro -- filtrada a las asignaturas reales de `Dr. Manuel Masías`, sin columna Profesorado (redundante cuando siempre es el mismo). **Antes extendía a `iniciarSesion()` directamente** (`<<extend>>`, condición `rol == Profesor`, issue #49); desde la discussion [#274](https://github.com/mmasias/pyCelda/discussions/274) la incluye [`abrirInicio()`](../abrirInicio/README.md) (`<<include>>`, incondicional -- el hub incorpora siempre las dos secciones) como sección "Mis guías". El listado de "mis asignaturas" no es un caso de uso nuevo, es este mismo, condicionado. `abrirInicio()` es lo que extiende a `iniciarSesion()`, invocado por `UsuarioNoLogueado`, no por `Profesor` -- el rol solo existe tras validar credenciales.

**Doble identidad `DirectorPrograma` + `Profesor`, subsumida por `abrirInicio()` (discussion [#274](https://github.com/mmasias/pyCelda/discussions/274))**: `DirectorPrograma` y `Profesor` son roles independientes, no exclusivos -- una misma persona puede tener fila en ambas tablas (caso real en dev: `manuel.masias@uneatlantico.es`). Entre 2026-08-22 y #274 esto se modeló como un **tercer punto de extensión** de este CU (`PROGRAMAS_ABIERTO --> ASIGNATURAS_PROGRAMA_ABIERTO`, condición `rol_sesion == DirectorPrograma AND existe fila propia en profesores`): un segundo camino desde el aterrizaje de `DirectorPrograma` hacia la variante filtrada por profesor. Ese tercer punto **desaparece**: `abrirInicio()` compone "Mis guías" y "Mis programas" en una sola pantalla, así que la doble identidad es simplemente "el hub con las dos secciones pobladas", no un punto de entrada aparte. Sigue sin ser un caso de uso ni un endpoint nuevo -- `GET /mis-asignaturas-programa` no cambia.

**Ambas páginas del mockup que reutilizan esta carpeta necesitan override manual**: sin él, el multi-wireframe del script mostraría las dos variantes en ambas páginas indiscriminadamente -- mismo riesgo ya corregido para `abrirGuia()` (commit `c006f5b`). `directorPrograma/abrirAsignaturasPrograma.md` muestra solo `wireframe.svg` (sin filtro); `profesor/iniciarSesion.md` muestra solo `wireframe-porProfesor.svg` (filtrada).

**Badge de color de estado (issue [#280](https://github.com/mmasias/pyCelda/issues/280))**: la columna `Estado` pasa a badge de color con caja "Leyenda" -- verde `Aprobada`, ámbar `EnRevision`, rojo `Rechazada`, neutro `Borrador`, etiqueta legible, color aditivo. Misma pieza (`estadoGuia.ts` + `EstadoGuiaBadge` + `LeyendaEstadosGuia`) que [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md). Aplica en **las dos variantes**: la de `Profesor` (`TablaMisGuias.tsx`, la que compone [`abrirInicio()`](../abrirInicio/README.md) y `/mis-asignaturas-programa`) y la de `DirectorPrograma` (`AsignaturasPrograma.tsx`, listado por-programa con Profesorado, que el director escanea igual que `consultarEstadoGuias()` -- dejarla en texto plano mientras su pantalla hermana tiene badges sería justo la inconsistencia que el feature elimina).

## Notas de diseño y trazabilidad

- El estado de la guía se muestra como badge de color (issue [#280](https://github.com/mmasias/pyCelda/issues/280)): etiqueta legible ("En revisión", no `EnRevision`) y color aditivo, sin sustituir al texto. Borrador, neutro; En revisión, ámbar; Aprobada, verde; Rechazada, rojo. El wireframe (Salt) no pinta fondos, por eso el color se documenta aquí y en la leyenda. La variante `DirectorPrograma` (`AsignaturasPrograma.tsx`) es un listado por Programa que el director escanea igual que [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md).

- Orden de la variante `DirectorPrograma`: curso, cuatrimestre y nombre, dentro de un Programa (issue [#290](https://github.com/mmasias/pyCelda/issues/290)).

- La variante `Profesor` es la que compone [`abrirInicio()`](../abrirInicio/README.md) y la pantalla `/mis-asignaturas-programa`. Sus filas se ordenan por cuatrimestre, curso, nombre y programa (planificación del profesor). La columna Curso combina curso y semestre en números romanos (`formatearCursoSemestre()`, issue [#508](https://github.com/mmasias/pyCelda/issues/508)): el issue [#292](https://github.com/mmasias/pyCelda/issues/292) había retirado esas columnas y el [#508](https://github.com/mmasias/pyCelda/issues/508) las reintroduce así. La columna Código (catálogo, 2026-09-30) sale de `Asignatura.codigo` vía `AsignaturaPrograma.asignatura_codigo` y puede mostrar "--" si `asignatura_id` no está resuelto.

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `PROGRAMA_ABIERTO --> ASIGNATURAS_PROGRAMA_ABIERTO : abrirAsignaturasPrograma()` (variante por-programa, con Profesorado); `INICIO_ABIERTO --> ASIGNATURAS_PROGRAMA_ABIERTO : abrirAsignaturasPrograma()` (variante por-profesor, deep link)
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `INICIO_ABIERTO --> ASIGNATURAS_PROGRAMA_ABIERTO : abrirAsignaturasPrograma()`; el aterrizaje tras el login es `INICIO_ABIERTO`
- [`abrirInicio()`](../abrirInicio/README.md) -- primitiva que `<<include>>` la variante por-profesor como sección "Mis guías"
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) -- catálogo de casos de uso de `DirectorPrograma` sobre `AsignaturaPrograma`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa, Asignatura .. AsignaturaPrograma`, `AsignaturaPrograma -- Profesor`
