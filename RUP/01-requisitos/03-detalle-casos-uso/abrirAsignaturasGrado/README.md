<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirAsignaturasGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturasGrado/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturasGrado/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorGrado`|
|**Objetivo**|Consultar el listado de `AsignaturaGrado` de un `Grado`, con el profesorado que las imparte|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

Propio de `DirectorGrado`, sin equivalente en `Admin`: el `Admin` no tiene un listado plural de `AsignaturaGrado`, accede a ellas desde el atajo plano embebido en [`abrirGrado()`](../abrirGrado/README.md) (retocado en este mismo lote). El `DirectorGrado`, en cambio, sí necesita ver de un vistazo todas las `AsignaturaGrado` de su `Grado` junto con el profesorado asignado (`AsignaturaGrado -- Profesor`, plantilla estable de impartición) -- de ahí el listado propio.

Columna **Profesorado**: dato ya presente en el modelo de dominio, mostrado en modo solo lectura -- la gestión de esa asignación (`asignarProfesorAAsignaturaGrado()`/`desasignarProfesorAsignaturaGrado()`, `Admin`) es de L6, todavía sin construir; no lleva botón propio en este listado.

Sin botón "Crear": `crearAsignaturaGrado()` es exclusivo de `Admin`, no de `DirectorGrado` (ver [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml)), mismo criterio que `abrirMaterias()` (`DirectorGrado` la reutiliza para navegar, pero `crearMateria()` sigue siendo de `Admin`).

**Retocado al planificar Análisis (discussion #47)**: columna `Estado` añadida, con las cuatro `Guia.estado` posibles representadas -- necesario para el caso de uso piloto de Análisis (Profesor viendo sus guías en sus distintos estados). Tres filas nuevas, todas datos reales verificados contra `docs/scripts/seed/raw.json` (curso académico 2026-2027, GII), no fabricadas por adivinanza -- mismo criterio que la fila original: `Estructuras de datos y algoritmos I` (`IYA025`, curso 2, Dr. Manuel Masías Vergara) y `Ingeniería de Software I` (`IYA038`, curso 3, Dr. Manuel Masías Vergara) coinciden en profesorado con la fila original; `Redes de Ordenadores` (`IYA022`, curso 2) es del Dr. Mariano Benito Hoz, profesor distinto -- verificado, no asumido por continuidad con las demás filas.

**Caso de uso parametrizado (issue #48)**: la fila con profesorado mezclado (`Dr. Manuel Masías` en tres filas, `Dr. Mariano Benito Hoz` en la cuarta) es exactamente correcta para `DirectorGrado`, que necesita ver todo el grado -- pero es la vista equivocada si se reutiliza sin más para `Profesor`, que solo debe ver sus propias `AsignaturaGrado`. De ahí la segunda variante, `wireframe-porProfesor.svg`: mismo caso de uso, invocado con un parámetro (el profesor que consulta) en vez de sin filtro -- filtrada a las asignaturas reales de `Dr. Manuel Masías`, sin columna Profesorado (redundante cuando siempre es el mismo). Es la variante que extiende a `iniciarSesion()` en el aterrizaje de `Profesor` -- `<<extend>>`, no `<<include>>` (condición `rol == Profesor`, ver issue #49) -- el listado de "mis asignaturas" no es un caso de uso nuevo, es este mismo, condicionado. `iniciarSesion()` la invoca `UsuarioNoLogueado`, no `Profesor` -- ver [README de `iniciarSesion()`](../iniciarSesion/README.md) para la corrección completa (error sistemático de la bibliografía RUP: el rol solo existe tras validar credenciales, no puede ser quien invoca la validación; y `<<include>>` es incondicional por definición, no encaja con una de tres ramas mutuamente excluyentes).

**Ambas páginas del mockup que reutilizan esta carpeta necesitan override manual**: sin él, el multi-wireframe del script mostraría las dos variantes en ambas páginas indiscriminadamente -- mismo riesgo ya corregido para `abrirGuia()` (commit `c006f5b`). `directorGrado/abrirAsignaturasGrado.md` muestra solo `wireframe.svg` (sin filtro); `profesor/iniciarSesion.md` muestra solo `wireframe-porProfesor.svg` (filtrada).

## Referencias

- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `GRADO_ABIERTO --> ASIGNATURAS_GRADO_ABIERTO : abrirAsignaturasGrado()`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- catálogo de casos de uso de `DirectorGrado` sobre `AsignaturaGrado`
- Modelo del dominio -- `Grado, Asignatura .. AsignaturaGrado`, `AsignaturaGrado -- Profesor`
