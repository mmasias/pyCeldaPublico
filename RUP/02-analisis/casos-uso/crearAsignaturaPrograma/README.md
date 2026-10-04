<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearAsignaturaPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearAsignaturaPrograma/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/crearAsignaturaPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`crearAsignaturaPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/crearAsignaturaPrograma/README.md): CRUD real e inmediato contra `AsignaturaProgramaRepository`, pero con cuatro colaboraciones de modelo donde el resto de `crearX()` tenía una. `AsignaturaPrograma` es la primera entidad del proyecto creada desde dos catálogos a la vez: el selector de `Materia` (las del `Programa`, vía [`crearMateria()`](../crearMateria/README.md), que fija la composición `Materia *-- AsignaturaPrograma`) y el selector de `Asignatura` (catálogo institucional plano, de donde se heredan `nombre`/`ects`/`contenido` si el `Admin` no los overridea in situ). La cuarta colaboración es el efecto colateral sobre `Guia` documentado en Requisitos: la `AsignaturaPrograma` nace con su `Guia` vacía en `Borrador`, delegando en `GuiaRepository`. Sin `<<choice>>`: las dos validaciones reales (la `Materia` existe y pertenece al `Programa` de la URL; la `Asignatura` existe en el catálogo) son guardas sobre identificadores que llegan de selectores poblados por el propio sistema, no reglas de negocio cruzadas. `estado` nace `Vigente` por defecto, sin pedirlo. Salida en self-loop sobre `PROGRAMA_ABIERTO`, excepción deliberada a la regla `<<include>> editarX()` del resto de `crearX()` (ver abajo).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/crearAsignaturaPrograma/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `CrearAsignaturaProgramaView`

**Responsabilidades:**
- presenta el selector de `Materia` del `Programa` (obligatorio) y el selector de `Asignatura` del catálogo (obligatorio).
- presenta `curso`, `carácter`, `idioma`, `semestre por defecto` -- obligatorios, sin valor de catálogo que heredar.
- presenta `nombre`/`ects`/`contenido` ya rellenos con el valor heredado de la `Asignatura` seleccionada, editables in situ para el override.
- permite solicitar crear.

**Colaboraciones:**
- **Entrada:** `:PROGRAMA_ABIERTO` -- el `Admin` solicita crear una `AsignaturaPrograma` desde la tabla embebida de la ficha del `Programa` (variante Admin de [`abrirPrograma()`](../abrirPrograma/README.md)).
- **Control:** `AsignaturaProgramaController`.
- **Salida:** `:PROGRAMA_ABIERTO` -- la nueva fila aparece en la tabla de `AsignaturaPrograma` de la ficha, sin `<<include>>`.

## Clases de controlador

### `AsignaturaProgramaController`

**Responsabilidades:**
- lista las `Materia` del `Programa` para el selector (`listarMateriasDelPrograma(programaId)`).
- lista las `Asignatura` del catálogo para el selector (`listarAsignaturasDelCatalogo()`).
- valida los obligatorios (`validarDatosObligatorios(materiaId, asignaturaId, curso, caracter, idioma, semestreDefault)`).
- crea la `AsignaturaPrograma` (`crearAsignaturaPrograma(...)`): verifica que la `Materia` pertenece al `Programa` de la llamada y que la `Asignatura` existe en el catálogo, resuelve la herencia de `nombre`/`ects`/`contenido` cuando no hay override, y delega en `AsignaturaProgramaRepository` con `estado` naciendo `Vigente`.
- crea la `Guia` vacía de la `AsignaturaPrograma` recién nacida (`crear(programaId, asignaturaProgramaId, semestreDefault)` sobre `GuiaRepository`) -- efecto colateral documentado en Requisitos: `Borrador`, `semestre = semestreDefault`, sin ponderaciones/referencias/profesorado.

**Colaboraciones:**
- **Entrada:** `CrearAsignaturaProgramaView`.
- **Salida:** `MateriaRepository`, `AsignaturaRepository`, `Asignatura`, `AsignaturaProgramaRepository`, `GuiaRepository`.

## Clases de modelo

### `Materia`

**Responsabilidades:**
- porta `nombre` y su `programaId` -- el controlador lo consulta para verificar la pertenencia al `Programa`.

**Colaboraciones:**
- **Entrada:** recuperada/listada por `MateriaRepository`.

### `MateriaRepository`

**Responsabilidades:**
- recupera la `Materia` por identificador (`obtener(materiaId)`) y lista las del `Programa` (`listarDelPrograma(programaId)`) -- ambos ya existentes.

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`.
- **Salida:** gestiona `Materia`.

### `Asignatura`

**Responsabilidades:**
- porta `nombre`, `ects`, `contenido` del catálogo -- el origen de los tres campos heredados-editables.

**Colaboraciones:**
- **Entrada:** recuperada/listada por `AsignaturaRepository`.

### `AsignaturaRepository`

**Responsabilidades:**
- recupera la `Asignatura` por identificador (`obtener(asignaturaId)`) y lista el catálogo (`listar()`) -- ambos ya existentes.

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`.
- **Salida:** gestiona `Asignatura`.

### `AsignaturaPrograma`

**Responsabilidades:**
- porta `nombre`, `curso`, `caracter`, `idioma`, `ects`, `semestreDefault`, `contenido` y su `materiaId` de composición desde el momento de crearse; `estado` nace `Vigente` sin pedirlo.

**Colaboraciones:**
- **Entrada:** creada por `AsignaturaProgramaRepository`.

### `AsignaturaProgramaRepository`

**Responsabilidades:**
- crea la `AsignaturaPrograma` (`crear(materiaId, nombre, curso, caracter, idioma, ects, semestreDefault, contenido)`) -- persistencia real e inmediata.

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`.
- **Salida:** gestiona `AsignaturaPrograma`.

### `Guia`

**Responsabilidades:**
- porta `estado` (nace `Borrador`), `semestre` (nace de `AsignaturaPrograma.semestreDefault`), `programaId` y su `asignaturaProgramaId` -- sin `PonderacionEvaluacion`, `ReferenciaBibliografica` ni profesorado: es la primera `Guia` de esta `AsignaturaPrograma`, no hay nada que clonar.

**Colaboraciones:**
- **Entrada:** creada por `GuiaRepository`.

### `GuiaRepository`

**Responsabilidades:**
- crea la `Guia` vacía (`crear(programaId, asignaturaProgramaId, semestre)`) -- misma forma que el nacimiento sin `Guia` anterior de `activarCursoAcademico()` (ver [modelo del dominio](/RUP/00-modelo-del-dominio/README.md), "Qué se clona exactamente al nacer una `Guia`...").

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`.
- **Salida:** gestiona `Guia`.

## Salida sin `<<include>> editarAsignaturaPrograma()`

**Excepción deliberada a la regla general de `crearX()`**: la salida no aterriza en `ASIGNATURA_PROGRAMA_ABIERTO` sino de vuelta en `PROGRAMA_ABIERTO` (self-loop, ver [diagramaContextoAdmin.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml): `PROGRAMA_ABIERTO --> PROGRAMA_ABIERTO : crearAsignaturaPrograma()`) -- la nueva fila aparece en la tabla de `AsignaturaPrograma` de la ficha del `Programa`. Y aunque aterrizara allí, `editarAsignaturaPrograma()` no es acción de `Admin` (que crea) sino de `DirectorPrograma` -- la regla del `<<include>>` asume que quien crea es quien edita a continuación; aquí no se cumple.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearAsignaturaPrograma/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/crearAsignaturaPrograma/wireframes.puml) -- fuente de verdad del formulario, incluida la corrección que añadió el selector de `Materia`.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROGRAMA_ABIERTO --> PROGRAMA_ABIERTO : crearAsignaturaPrograma()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Materia *-- AsignaturaPrograma`; herencia de `nombre`/`ects`/`contenido` sobre `Asignatura`.
- [`crearMateria()`](../crearMateria/README.md) -- puebla el selector de `Materia`, construido en este mismo lote.
- [`eliminarAsignaturaPrograma()`](../eliminarAsignaturaPrograma/README.md) -- la otra acción sobre la misma tabla embebida, construida en este mismo lote.
- [`abrirPrograma()`](../abrirPrograma/README.md) -- la ficha cuyo retoque añade la tabla desde la que se dispara este caso de uso.
- [`crearPrograma()`](../crearPrograma/README.md) -- contraste: `crearX()` con `<<include>>` de salida, la regla que aquí no aplica.
