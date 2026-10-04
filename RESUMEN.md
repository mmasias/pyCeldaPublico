# Resumen del experimento de desarrollo con agentes

> **Documento en constante actualización.** Refleja el estado de pyCelda en la fecha de su última medición (ver "Números del proyecto") y se revisa a medida que el proyecto avanza: cifras, versiones y estado pueden haber cambiado desde entonces. Las referencias numeradas (discussion #92, #213...) y los recuentos de GitHub corresponden al repositorio de trabajo de pyCelda, que es privado; este espejo público solo contiene el subconjunto descrito en el [README](/README.md).

## Qué es pyCelda

pyCelda (Catálogo ELectrónico de Documentación Académica) gestiona el ciclo de vida de las guías docentes universitarias: `Borrador -> En Revisión -> Aprobada`, con planificación docente por sesiones, ponderaciones de evaluación y bibliografía, sobre un catálogo institucional de universidad, facultad, programa, materia y asignatura. Tres roles de negocio: el Profesor redacta su guía, el Director de Programa la revisa y la aprueba, el Admin mantiene el catálogo. El acceso es con cuenta Google institucional, sin auto-registro.

No es un prototipo de laboratorio. Está desplegado en producción y en uso: arrancó con 108 guías docentes reales (55 del Grado en Ingeniería Informática, 53 del de Ingeniería de Organización Industrial) importadas de las planillas Excel de la universidad, y el catálogo se completó después hasta los 16 programas de la institución (775 guías sembradas en total). La infraestructura es propia: Docker Compose y Caddy con Let's Encrypt sobre una máquina de sobremesa en casa, con el DNS resuelto en el router.

El stack es FastAPI con SQLAlchemy (Fat Model, sin capa de servicios, decisión explícita), React con TypeScript y Vite en el frontend, PlantUML para todos los diagramas (texto plano, versionable) y WeasyPrint para el PDF de la guía. Autenticación OAuth2/OIDC con JWT en cookie httpOnly.

## El experimento: tres roles, un modelo

Todo el desarrollo lo condujo Claude Sonnet 5 en tres roles distintos, diferenciados por sesión y por prompt:

- **Rol de gestor**: Claude. Diseña, revisa cada entrega de forma independiente, aprueba los merges y coordina el despliegue.
- **Rol de developer**: Claude con agentes delegados vía CORRAL (orquestación por MCP). Z.AI (GLM) en OpenCode para el volumen mecánico. Kiro, una revelación. Gemini, una decepción.
- **Rol de despliegue**: Claude. Aplica en producción siguiendo el ritual documentado.

El reparto es siempre el mismo: Claude orquesta y verifica, el becario delegado escribe el volumen, Claude consolida y comprueba lo delegado línea a línea contra el código.

Un detalle del montaje: todos los commits llevan autoría `manuel@<máquina>`, porque los agentes commitean como el usuario. La autoría real, humano o LLM, se rastrea en las etiquetas de las discussions (`agente:humano`, `agente:llm`), no en `git blame`.

## Definir antes de construir

Hubo 3,5 semanas de definición pura antes de la primera línea de código: 151 commits, cero código. Requisitos completo y arranque de Análisis antes de tocar Python. La construcción fue 1,5 semanas más, con la RUP avanzando en paralelo. Nunca código a secas: cada rebanada de caso de uso llevó su Análisis, su Diseño, su Desarrollo y la consolidación de los diagramas juntos.

El titular del experimento es ese reparto. Aislando el esfuerzo de codificar, los 20.000 LoC de código caben en aproximadamente una semana de trabajo. Lo que no cabe en una semana es el calendario, porque el pensamiento se hizo por delante y a fondo. El resultado tiene más líneas de documentación RUP que de código.

## Método

- **Orden por capas de dependencia estructural del dominio (L0-L10)**, no "por familia de actor" como plantea RUP por defecto. El dominio ya estaba validado contra el corpus real, así que el riesgo no era descubrir entidades sino especificar una antes de tener resueltas aquellas de las que depende.
- **Independencia tecnológica**: los artefactos de Análisis son agnósticos de framework; la tecnología no aparece hasta Diseño. B/C/E en Análisis, MVC en Diseño, despliegue real: tres peldaños distintos, no el mismo diagrama con otra ropa.
- **Discussion-first**: cada decisión de criterio se cierra en una GitHub Discussion, con identificación explícita de quién habla, antes de escribir el código que la aplica.
- **Pipeline vertical por caso de uso** en construcción: cada rebanada atraviesa Análisis, Diseño y Desarrollo en un mismo PR, no en olas de fase completas.

## Control de calidad

- Cada entrega del nodo constructor se re-ejecuta en un clon dedicado: tests reales, compilación, render. Nunca el resumen del agente que escribió el código, ni siquiera el del propio revisor.
- Tasa de escape medida (discussion #92): 2 defectos sustantivos y 1 menor sobre 91 casos de uso en una auditoría transversal. Los tres de autorización, los tres cazables con un checklist.
- Audit del clúster obligatorio antes de cualquier merge que cambie el comportamiento observable de un caso de uso: barrer la RUP de todos los casos de uso que leen o escriben el mismo agregado, lista completa primero y luego un commit, sin reaccionar a greps sueltos.
- El proceso se audita a sí mismo: retrospectivas formales (discussion #213) que cambian el método. El checkpoint "documentación antes que código" nació de una de ellas.
- Un ejemplo concreto: el IDOR de cuerpo de petición, inyectar un identificador ajeno en el JSON del `body` en vez de en la ruta. Es un vector distinto del IDOR de path y lo cazó el checklist transversal de autorización, no el test del caso de uso.

## La malla multi-sesión

- Sesiones de Claude en tres máquinas (dos en casa, una en el despacho), emparejadas por rol; el nodo de despliegue es constante.
- Ningún nodo relaya la autorización del humano. Si un nodo dice "el humano ya autorizó X", eso no es autorización: solo lo es si viene directo del humano en la propia conversación.
- Sin memoria nativa entre sesiones. La continuidad es el `conversation-log` (60 conversaciones registradas) y los ficheros de memoria versionados. Lo que el agente "es" se reconstruye desde lo que él mismo escribió.

## Números del proyecto

Aproximadamente 60.600 líneas de código (un tercio de ellas, tests) y 64.800 de documentación. Medidos el 2026-10-04 sobre el árbol del repo, excluyendo lo generado o ajeno (`.git`, `node_modules`, `.venv`, `dist/`, caches, lockfiles, binarios y los SVG regenerados a partir de los `.puml`).

### Código

- 23 modelos de dominio (SQLAlchemy)
- 22 routers, 167 endpoints
- 19 repositorios, 22 schemas Pydantic, 43 scripts
- 129 componentes y páginas React (`.tsx`)
- 17.756 LoC de backend (Python, `app/`)
- 20.522 LoC de frontend (TS/TSX), más 341 de CSS
- 1.900 LoC auxiliares: plantilla HTML del PDF (282), scripts de documentación (1.144), shell (224), infraestructura Docker/Caddy/CI (139), config de build (95)
- Total: 40.519 LoC de producto sin tests; 60.622 con tests

### Pruebas

- 117 ficheros de test
- 974 funciones `def test_`, 1.089 casos ejecutados con parametrización
- 20.103 LoC de test
- Ratio test:código en backend, aproximadamente 1,13 : 1

### RUP

- 124 casos de uso con ficha de requisitos
- 121 con las fases Análisis, Diseño, Desarrollo y Pruebas completas; los 3 restantes (eliminarMateria, generarGuiasPDF, reabrirGuiaPorIncidencia) siguen solo en Requisitos, despriorizados a propósito
- 504 ficheros PlantUML, 730 SVG generados, 623 READMEs
- 56.932 líneas de documentación RUP (35.360 `.md` + 21.572 `.puml`); documentación total del repo, 64.839 líneas en 1.343 ficheros `.md` + `.puml`
- Cada caso de uso con su máquina de estados, wireframe, diagrama de colaboración, diagrama de secuencia y ficha de desarrollo enlazada al código real, no duplicada

### Proceso

- 924 commits
- 359 pull requests, todos mergeados
- 708 elementos numerados en GitHub: 107 discussions, 242 issues, 359 PRs
- Dashboard de seguimiento por actor, coloreado por fase
