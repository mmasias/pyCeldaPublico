<div align=right><sub>Volver: [Al inicio](/README.md) / [#2think](2Think.md) · [Análisis](/RUP/02-analisis/README.md)</sub></div>

# Dónde vive cada regla: Modelo, Controlador y Repositorio en pyCelda

> Nota de referencia para la fase de Análisis. Escrito al cierre de Requisitos, cuando `modeloDominio.puml` y las 91 especificaciones de casos de uso ya dejaban claro *qué* reglas existen y *quién* las dispara — lo que faltaba resolver era *dónde viven* una vez eso se convierta en código.

## La pregunta

`pyCelda` tiene reglas de negocio con peso real: la suma de `PonderacionEvaluacion` debe dar exactamente 100%, los `ResultadoAprendizaje` de una `AsignaturaGrado` deben ser subconjunto de los de su `Materia`, una `Guia` puede volver a revisión por cuatro caminos distintos según quién y por qué. Hoy, cada una de esas reglas vive en un solo sitio: la especificación PlantUML del caso de uso que la dispara. Al pasar a código con MVC, la pregunta es simple de formular y fácil de responder mal: **¿esas reglas se centralizan en un único sitio también, o se reparten según a quién le toque programar cada uno de los 91 casos?**

Si se reparten, el riesgo no es hipotético — es el mismo tipo de grieta que las auditorías de esta fase ya demostraron que sabéis cazar (la nota fantasma en `crearGrado/README.md`, el `codigo` de `Asignatura` que se quedó fuera de su propio CRUD). Solo que en código, en vez de una frase de README desactualizada, sería la regla del 100% implementada una vez en `enviarGuiaARevision()` y de otra forma, ligeramente distinta, el día que alguien necesite comprobarla desde otro sitio.

## El error que lleva ahí sin querer

La confusión más común no es pereza, es una equivalencia que parece inocente y no lo es: **igualar "Modelo" con "la capa que habla con la base de datos".**

Son primos, no la misma persona. En MVC, el Modelo es la capa de **dominio** — objetos con comportamiento propio, no solo contenedores de datos. La capa de persistencia (el ORM, las consultas SQL) es otra cosa distinta, normalmente escondida detrás de un Repositorio. Si se confunden las dos, el razonamiento parece lógico pero lleva al sitio equivocado: "no quiero que la base de datos cargue con lógica de negocio" → se saca la lógica del Modelo → aterriza suelta en los controladores, uno por caso de uso, sin nadie centralizándola.

Esto tiene nombre en la literatura: **modelo anémico** (*anemic domain model*, Martin Fowler). Es un Modelo que solo tiene atributos y getters/setters, sin ningún método que exprese una regla propia — toda la inteligencia vive fuera, repartida. Es exactamente el antipatrón que convertiría los meses invertidos en `modeloDominio.puml` — con sus cascadas, sus validaciones, sus estados — en un conjunto de tablas sin memoria una vez llegue el código, obligando a reinventar ese comportamiento en otro sitio, caso de uso a caso de uso.

## Por qué el Repositorio tampoco es el sitio

Una tercera tentación, igual de comprensible: si ni el controlador ni el modelo-tabla parecen el sitio correcto, meter la validación en el Repositorio, "de paso" al guardar o leer.

El Repositorio, por definición, abstrae **cómo se llega a los datos** (hoy SQL, mañana memoria en un test, da igual) — no **si esos datos son correctos**. Si además valida, ya no hay dos candidatos a "dónde vive la regla", hay tres: controlador, repositorio, y el modelo conceptual que se supone que no es código. Eso no es indirección, es la misma pregunta sin resolver con una caja más donde esconderla.

## La regla: *Fat Model, Thin Controller*

No es una receta nueva — es vieja y está bien probada, y es la que resuelve esto sin ambigüedad:

- **El Modelo** (las clases de dominio en código — `Guia`, no la fila de la tabla `guia`) lleva el comportamiento y las reglas. Un método como `Guia.puedeSerAprobada()` o `PonderacionEvaluacion.sumaValida()` vive ahí, con la misma responsabilidad que ya tiene en `especificacion.puml`.
- **El Controlador** recibe la petición, llama al método del modelo que corresponde, y devuelve la respuesta. No decide nada — solo orquesta.
- **El Repositorio** hace una sola cosa: guardar y recuperar. No opina sobre si lo que guarda es válido — esa validación ya pasó antes, en el modelo.

Una sola caja con la regla. Dos cajas tontas alrededor.

## Aplicado a pyCelda: dónde caería cada regla ya conocida

| Regla (ya cerrada en `modeloDominio.puml` / especificaciones) | Vive en |
|-|-|
| Suma de `PonderacionEvaluacion` == 100% | `Guia.sumaPonderacionesValida()` o equivalente en `PonderacionEvaluacion` |
| `ResultadoAprendizaje` de `AsignaturaGrado` ⊆ los de su `Materia` | Método de validación en `AsignaturaGrado` al asociar un RA |
| `(Grado, Asignatura)` único como clave de `AsignaturaGrado` | Invariante del propio modelo, no una comprobación ad-hoc en el controlador de `crearAsignaturaGrado()` |
| Las cuatro transiciones de reapertura de `Guia` (`Aprobada` → `Borrador`/`EnRevision` según quién y por qué) | Métodos propios de `Guia`, con los mismos nombres ya catalogados (`revocarAprobacionGuia()`, `reabrirGuiaPorIncidencia()`...), no un `if` disperso en cada controlador que la dispara |
| `eliminarX()` bloqueado si tiene hijos | Método de comprobación en la propia entidad padre, que el controlador solo consulta antes de decidir la respuesta |

La correspondencia no es casualidad: cada `especificacion.puml` ya dice, sin ambigüedad, quién es responsable de cada regla — el Análisis no inventa esa asignación, la hereda.

## Cuando no hay un dueño obvio

La heurística "¿qué entidad ya es dueña de este dato?" funciona limpia para reglas de una sola entidad, pero al menos una regla ya cerrada la rompe: *"el `SistemaEvaluacion` al que apunta cada `PonderacionEvaluacion` de una Guía debe pertenecer a la misma `Materia` que la `AsignaturaGrado` de esa Guía"* cruza tres entidades sin que ninguna sea la propietaria natural — ni `PonderacionEvaluacion`, ni `SistemaEvaluacion`, ni `AsignaturaGrado` "poseen" esta regla más que las otras.

Para este caso, y cualquier otro con la misma forma, el criterio de desempate no es "quién es dueño", es **quién es el punto de entrada de la operación** — aquí, `Guia`, que es quien agrega la `PonderacionEvaluacion` y por tanto quien tiene tanto el dato nuevo como el contexto (su propia `AsignaturaGrado`) para poder comprobar la regla en el mismo sitio.

## Qué significa esto para el Análisis

Al pasar de especificación a diseño de clases, la pregunta que conviene hacerse por cada `<<choice>>` y cada regla de negocio del modelo no es *"¿en qué capa técnica lo pongo?"* — es *"¿qué entidad del dominio ya es dueña de este dato en `modeloDominio.puml`?"*. Esa entidad es la que lleva el método. El controlador la llama; el repositorio la persiste sin preguntar.