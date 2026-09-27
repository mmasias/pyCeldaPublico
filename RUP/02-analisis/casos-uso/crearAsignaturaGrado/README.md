<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > crearAsignaturaGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearAsignaturaGrado/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/crearAsignaturaGrado/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`crearAsignaturaGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/crearAsignaturaGrado/README.md): CRUD real e inmediato contra `AsignaturaGradoRepository`, pero con cuatro colaboraciones de modelo donde el resto de `crearX()` tenía una. `AsignaturaGrado` es la primera entidad del proyecto creada desde dos catálogos a la vez: el selector de `Materia` (las del `Grado`, vía [`crearMateria()`](../crearMateria/README.md), que fija la composición `Materia *-- AsignaturaGrado`) y el selector de `Asignatura` (catálogo institucional plano, de donde se heredan `nombre`/`ects`/`contenido` si el `Admin` no los overridea in situ). La cuarta colaboración es el efecto colateral sobre `Guia` documentado en Requisitos: la `AsignaturaGrado` nace con su `Guia` vacía en `Borrador`, delegando en `GuiaRepository`. Sin `<<choice>>`: las dos validaciones reales (la `Materia` existe y pertenece al `Grado` de la URL; la `Asignatura` existe en el catálogo) son guardas sobre identificadores que llegan de selectores poblados por el propio sistema, no reglas de negocio cruzadas. `estado` nace `Vigente` por defecto, sin pedirlo. Salida en self-loop sobre `GRADO_ABIERTO`, excepción deliberada a la regla `<<include>> editarX()` del resto de `crearX()` (ver abajo).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/crearAsignaturaGrado/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `CrearAsignaturaGradoView`

**Responsabilidades:**
- presenta el selector de `Materia` del `Grado` (obligatorio) y el selector de `Asignatura` del catálogo (obligatorio).
- presenta `curso`, `carácter`, `idioma`, `semestre por defecto` -- obligatorios, sin valor de catálogo que heredar.
- presenta `nombre`/`ects`/`contenido` ya rellenos con el valor heredado de la `Asignatura` seleccionada, editables in situ para el override.
- permite solicitar crear.

**Colaboraciones:**
- **Entrada:** `:GRADO_ABIERTO` -- el `Admin` solicita crear una `AsignaturaGrado` desde la tabla embebida de la ficha del `Grado` (variante Admin de [`abrirGrado()`](../abrirGrado/README.md)).
- **Control:** `AsignaturaGradoController`.
- **Salida:** `:GRADO_ABIERTO` -- la nueva fila aparece en la tabla de `AsignaturaGrado` de la ficha, sin `<<include>>`.

## Clases de controlador

### `AsignaturaGradoController`

**Responsabilidades:**
- lista las `Materia` del `Grado` para el selector (`listarMateriasDelGrado(gradoId)`).
- lista las `Asignatura` del catálogo para el selector (`listarAsignaturasDelCatalogo()`).
- valida los obligatorios (`validarDatosObligatorios(materiaId, asignaturaId, curso, caracter, idioma, semestreDefault)`).
- crea la `AsignaturaGrado` (`crearAsignaturaGrado(...)`): verifica que la `Materia` pertenece al `Grado` de la llamada y que la `Asignatura` existe en el catálogo, resuelve la herencia de `nombre`/`ects`/`contenido` cuando no hay override, y delega en `AsignaturaGradoRepository` con `estado` naciendo `Vigente`.
- crea la `Guia` vacía de la `AsignaturaGrado` recién nacida (`crear(gradoId, asignaturaGradoId, semestreDefault)` sobre `GuiaRepository`) -- efecto colateral documentado en Requisitos: `Borrador`, `semestre = semestreDefault`, sin ponderaciones/referencias/profesorado.

**Colaboraciones:**
- **Entrada:** `CrearAsignaturaGradoView`.
- **Salida:** `MateriaRepository`, `AsignaturaRepository`, `Asignatura`, `AsignaturaGradoRepository`, `GuiaRepository`.

## Clases de modelo

### `Materia`

**Responsabilidades:**
- porta `nombre` y su `gradoId` -- el controlador lo consulta para verificar la pertenencia al `Grado`.

**Colaboraciones:**
- **Entrada:** recuperada/listada por `MateriaRepository`.

### `MateriaRepository`

**Responsabilidades:**
- recupera la `Materia` por identificador (`obtener(materiaId)`) y lista las del `Grado` (`listarDelGrado(gradoId)`) -- ambos ya existentes.

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`.
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
- **Entrada:** `AsignaturaGradoController`.
- **Salida:** gestiona `Asignatura`.

### `AsignaturaGrado`

**Responsabilidades:**
- porta `nombre`, `curso`, `caracter`, `idioma`, `ects`, `semestreDefault`, `contenido` y su `materiaId` de composición desde el momento de crearse; `estado` nace `Vigente` sin pedirlo.

**Colaboraciones:**
- **Entrada:** creada por `AsignaturaGradoRepository`.

### `AsignaturaGradoRepository`

**Responsabilidades:**
- crea la `AsignaturaGrado` (`crear(materiaId, nombre, curso, caracter, idioma, ects, semestreDefault, contenido)`) -- persistencia real e inmediata.

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`.
- **Salida:** gestiona `AsignaturaGrado`.

### `Guia`

**Responsabilidades:**
- porta `estado` (nace `Borrador`), `semestre` (nace de `AsignaturaGrado.semestreDefault`), `gradoId` y su `asignaturaGradoId` -- sin `PonderacionEvaluacion`, `ReferenciaBibliografica` ni profesorado: es la primera `Guia` de esta `AsignaturaGrado`, no hay nada que clonar.

**Colaboraciones:**
- **Entrada:** creada por `GuiaRepository`.

### `GuiaRepository`

**Responsabilidades:**
- crea la `Guia` vacía (`crear(gradoId, asignaturaGradoId, semestre)`) -- misma forma que el nacimiento sin `Guia` anterior de `activarCursoAcademico()` (ver [modelo del dominio](/RUP/00-modelo-del-dominio/README.md), "Qué se clona exactamente al nacer una `Guia`...").

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`.
- **Salida:** gestiona `Guia`.

## Salida sin `<<include>> editarAsignaturaGrado()`

**Excepción deliberada a la regla general de `crearX()`**: la salida no aterriza en `ASIGNATURA_GRADO_ABIERTO` sino de vuelta en `GRADO_ABIERTO` (self-loop, ver [diagramaContextoAdmin.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml): `GRADO_ABIERTO --> GRADO_ABIERTO : crearAsignaturaGrado()`) -- la nueva fila aparece en la tabla de `AsignaturaGrado` de la ficha del `Grado`. Y aunque aterrizara allí, `editarAsignaturaGrado()` no es acción de `Admin` (que crea) sino de `DirectorGrado` -- la regla del `<<include>>` asume que quien crea es quien edita a continuación; aquí no se cumple.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearAsignaturaGrado/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/crearAsignaturaGrado/wireframes.puml) -- fuente de verdad del formulario, incluida la corrección que añadió el selector de `Materia`.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `GRADO_ABIERTO --> GRADO_ABIERTO : crearAsignaturaGrado()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Materia *-- AsignaturaGrado`; herencia de `nombre`/`ects`/`contenido` sobre `Asignatura`.
- [`crearMateria()`](../crearMateria/README.md) -- puebla el selector de `Materia`, construido en este mismo lote.
- [`eliminarAsignaturaGrado()`](../eliminarAsignaturaGrado/README.md) -- la otra acción sobre la misma tabla embebida, construida en este mismo lote.
- [`abrirGrado()`](../abrirGrado/README.md) -- la ficha cuyo retoque añade la tabla desde la que se dispara este caso de uso.
- [`crearGrado()`](../crearGrado/README.md) -- contraste: `crearX()` con `<<include>>` de salida, la regla que aquí no aplica.
