# No es *vibe coding*

> Cómo se construye pyCelda con agentes de IA y por qué el resultado no depende de que "parezca que funciona".

## ¿Por qué?

En febrero de 2025 Andrej Karpathy puso nombre a una forma de programar con modelos de lenguaje: *"There's a new kind of coding I call 'vibe coding', where you fully give in to the vibes, embrace exponentials, and forget that the code even exists"* ([mensaje original](https://x.com/karpathy/status/1886192184808149383)). En el mismo mensaje describía el método: aceptar todos los cambios sin leer los diffs y, cuando algo falla, devolverle el error al modelo hasta que deje de fallar. El término se ha extendido para nombrar cualquier software construido pidiéndole cosas a un modelo y aceptando lo que sale mientras funcione.

pyCelda se escribe, en su mayor parte, con agentes de IA: varias sesiones de Claude Code con papeles distintos y, para el trabajo mecánico, OpenCode. Visto desde fuera puede parecer lo mismo. No lo es y la diferencia no es un matiz:

- En el *vibe coding*, que el resultado sea correcto depende de la probabilidad de que el texto generado lo sea. Nadie puede explicar por qué el sistema hace lo que hace ni darse cuenta de cuándo deja de hacerlo. El éxito queda reducido a estadística con esteroides.
- La ingeniería del software nunca consistió en teclear código. Consiste en decidir qué hay que construir, comprobar que lo construido hace eso y poder responder de ello. Llamar ingeniería a lo primero vacía de contenido la profesión.

Además, lo que gestiona pyCelda no admite "parece que funciona": guías docentes sujetas a la memoria verificada de cada programa, que redacta profesorado real, revisan directores de programa reales y acaban en manos del alumnado.

## ¿Qué?

El modelo de lenguaje es el mismo en los dos casos. Lo que cambia es todo lo que lo rodea.

<div align=center>

| | *Vibe coding* | pyCelda |
|-|-|-|
| **Qué se construye** | Lo que se pide en el momento | Lo especificado antes: modelo del dominio y 136 casos de uso en [`RUP/`](../../RUP/README.md), con especificación y wireframe |
| **Quién decide** | El modelo rellena los huecos | El director del proyecto decide cada bifurcación; los agentes la plantean con datos y alternativas |
| **Quién verifica** | El mismo que genera, mirando si arranca | Otro agente, ejecutando los tests en una copia aparte y contrastando con la especificación |
| **El código** | No se lee | Se lee el diff entero antes de fusionar |
| **Los errores** | Se pega el error hasta que desaparece | Se registra el issue, se busca la causa, se corrige el método si el método falló |
| **El rastro** | Una conversación que se pierde | Issue, discussion, PR, commit y bitácora de despliegue enlazados entre sí |
| **Producción** | Se despliega lo generado | Despliegue separado, migraciones probadas contra copia de la base de datos real, ninguna escritura en producción sin confirmación humana |

</div>

Un PR escrito por un agente se acepta por las mismas razones que uno escrito por una persona: cumple lo especificado, alguien distinto de su autor lo ha verificado ejecutándolo y queda trazado. El proceso hace que el resultado sea comprobable con independencia de quién o qué lo generó.

## ¿Para qué?

Lo que compra el método, medido sobre el propio repositorio:

<div align=center>

| Qué aporta | Evidencia |
|-|-|
| **Desarrollo sin decisiones** | 6 días de requisitos (41% de la actividad del primer tramo) y después 43 casos de uso implementados y desplegados en 72 horas. Ningún retroceso desde Desarrollo reabrió una decisión de Requisitos ([#92](https://github.com/mmasias/pyCelda/discussions/92)) |
| **Delegar sin perder el control** | Solo se puede delegar en un agente lo que ya está decidido y solo se puede verificar de forma mecánica lo que está especificado: requisitos -> decidibilidad -> delegabilidad -> velocidad ([#92](https://github.com/mmasias/pyCelda/discussions/92)) |
| **Errores pequeños y tempranos** | Unas 13 correcciones en 21 días, entre el 8% y el 10% del esfuerzo. Defectos que se escaparon hasta Desarrollo: 2 sustantivos y 1 menor sobre 91 casos de uso, los dos sustantivos de autorización transversal ([#92](https://github.com/mmasias/pyCelda/discussions/92)) |
| **Velocidad como consecuencia** | Ciclos completos de hallazgo a despliegue en minutos en cambios pequeños, porque la pregunta "¿qué debería pasar aquí?" ya estaba contestada y la confianza entre papeles se había ganado cazando errores reales, no se había supuesto ([#112](https://github.com/mmasias/pyCelda/discussions/112)) |
| **Poder responder** | Cualquier comportamiento del sistema enlaza con la decisión que lo fijó: quién la tomó, cuándo y con qué datos |

</div>

Son mediciones de un solo proyecto, sin grupo de control: indican, no demuestran. La propia [#92](https://github.com/mmasias/pyCelda/discussions/92) propone contrastarlas, primero en otro proyecto y después comparando lotes tempranos y tardíos del propio pyCelda.

## ¿Cómo?

### Los papeles

<div align=center>

| Papel | Hace | No hace |
|-|-|-|
| **Director del proyecto** (humano) | Decide producto y criterio. Autoriza toda escritura en la base de datos de producción | Delegar esas dos cosas |
| **Orquestador y revisor** (agente) | Plantea cada problema con datos y alternativas, redacta el encargo, verifica por su cuenta lo construido, fusiona y publica la versión | Decidir producto. Aprobar lo que ha escrito él mismo |
| **Constructor** (agente) | Implementa en una rama a partir de un issue autocontenido: documentación RUP, código, tests y versión | Fusionar ni desplegar |
| **Despliegue** (agente en la máquina de producción) | Copia de seguridad, despliegue, verificación de solo lectura y bitácora | Escribir datos sin confirmación |

</div>

Dos reglas sostienen el reparto: quien construye no se revisa a sí mismo y quien revisa no se fía del resumen del constructor, sino que repite las pruebas.

### El ciclo, sobre un caso real

La [discussion #206](https://github.com/mmasias/pyCelda/discussions/206) (septiembre de 2026) recorre el ciclo completo, con su retrospectiva en [#213](https://github.com/mmasias/pyCelda/discussions/213). El problema: qué condiciones debe cumplir una guía para poder enviarse a revisión, el paso central del flujo.

<div align=center>

| Paso | Qué pasó |
|-|-|
| **1. Problema real** | Tras probar la aplicación con profesorado real, el director del proyecto pide dos ajustes: un mínimo de sesiones planificadas para poder enviar la guía (propone 30) y ver la suma de las ponderaciones sin tener que hacerla de cabeza |
| **2. Planteamiento con datos** | El orquestador comprueba que las 5 guías del piloto tienen entre 26 y 29 sesiones: un mínimo de 30 las bloquearía todas. Descubre además que las sesiones no seguían el mismo mecanismo de guardado que el resto de la guía |
| **3. Decisión humana** | Respuestas de una línea a cada bifurcación: umbral entre 25 y 30 configurable por el Admin, alinear las sesiones con el resto, nueva condición de rechazo encadenada al final, medidor con total y subtotales en texto ("gráficos las huifas") |
| **4. Decisión escrita antes del código** | Las decisiones quedan cerradas en la discussion antes de construir. La especificación con tres comprobaciones encadenadas, los wireframes de cada rechazo, el Análisis y el Diseño se actualizan en el mismo PR que el código |
| **5. Construcción por bloques** | Tres PR de menos a más riesgo ([#207](https://github.com/mmasias/pyCelda/pull/207), [#209](https://github.com/mmasias/pyCelda/pull/209), [#211](https://github.com/mmasias/pyCelda/pull/211)). Los dos primeros llegan al profesorado antes de que el tercero añada la regla que bloquea el envío |
| **6. Verificación independiente** | El revisor ejecuta los tests en su propia copia (de 408 a 435), comprueba que lo servido en producción es idéntico byte a byte a lo que compila él y devuelve trabajo cuando falta algo. Afloran dos defectos anteriores al cambio: [#208](https://github.com/mmasias/pyCelda/issues/208), que caza el revisor, y [#210](https://github.com/mmasias/pyCelda/issues/210), de seguridad, que el constructor señala y el revisor registra |
| **7. Migración probada** | Antes de tocar producción se ensaya contra una copia de la base de datos real: 108 guías, ninguna fuera de rango. La ejecución final la lanza el director del proyecto |
| **8. Retrospectiva** | [#213](https://github.com/mmasias/pyCelda/discussions/213) analiza lo que salió mal (documentación aprobada a medias, una afirmación sin comprobar que cazó el constructor, cuatro rondas de correcciones donde bastaba una) y cambia el método: antes de fusionar se revisan todos los documentos afectados, no solo los tocados. En los PR que saldaron la deuda pendiente, ese barrido encontró 4 huecos en uno y 6 en otro |

</div>

### Lo que el método no evitó

Contar solo lo que salió bien sería hacer propaganda. Dos defectos ligados a esta regla llegaron a producción:

- **Dos cifras para lo mismo.** En el paso 3 se decidió que el medidor contara lo guardado y lo pendiente de guardar. Era coherente: el envío rechaza antes cualquier elemento sin guardar y el director veía la misma pantalla que el profesor. A finales de septiembre se añadió a la vista del director un resumen de completitud que cuenta solo lo guardado ([#504](https://github.com/mmasias/pyCelda/issues/504)) y nadie contrastó las dos cuentas. Dos meses más tarde, una directora que también es profesora vio un 100% en una pantalla y un aviso de suma incorrecta en otra: *"los porcentajes me dan una suma de 100% pero en la pantalla inicial me indica que debo revisarlo"* ([#842](https://github.com/mmasias/pyCelda/issues/842)). Se resolvió mostrando las dos cifras por separado y señalando con qué papel se mira cada pantalla de director y de docente ([#841](https://github.com/mmasias/pyCelda/issues/841), [#846](https://github.com/mmasias/pyCelda/issues/846)).
- **Coma flotante.** Desde agosto, la regla del 100% sumaba en coma flotante y comparaba con igualdad exacta: `3.12 + 72.68 + 4.28 + 19.92` da `100.00000000000001` y la guía no se podía enviar. La revisión de #206 tuvo esa comparación delante, la dio por buena y el medidor nuevo la replicó en el frontend. Lo encontró casi tres meses después otra revisión y se corrigió en la causa, con aritmética exacta en backend y frontend, no en el síntoma ([#849](https://github.com/mmasias/pyCelda/issues/849)).

La diferencia con el *vibe coding* no es la ausencia de errores. Es que cada error se puede explicar (dónde se decidió, por qué, quién lo revisó y qué se le escapó) y se corrige donde nació.

### Qué hacer y qué evitar

<div align=center>

| Hacer | Evitar |
|-|-|
| Especificar antes de construir y actualizar la documentación en el mismo PR que el código | Construir a partir de la conversación del momento |
| Separar autor y revisor. Verificar ejecutando, no leyendo el resumen | Que un agente apruebe su propio trabajo |
| Comprobar en la fuente antes de afirmar | Dar por buena una cita de otro agente o un documento sin abrir el original |
| Dar los pasos irreversibles (fusión, versión, migración, escritura en producción) por separado y con confirmación humana | Encadenar fusión, versión y despliegue en una sola orden |
| Un encargo, un issue autocontenido. Toda decisión queda escrita en el repositorio | Decisiones que solo existen en una conversación |
| Ante un defecto, revisar todo lo afectado y la causa | Corregir lo que encontró la búsqueda de hoy y esperar a la siguiente |

</div>

## ¿Y ahora qué?

El método tiene un coste: es más lento al principio y exige que alguien con criterio esté presente para decidir. Ese coste es justo lo que separa construir software de generarlo. Un modelo de lenguaje no sabe qué necesita un director de programa ni responde ante él. Esa parte del trabajo sigue siendo de la profesión.

**Referencias**

- Karpathy, A. [Mensaje que acuña "vibe coding"](https://x.com/karpathy/status/1886192184808149383), 2 de febrero de 2025.
- [#206](https://github.com/mmasias/pyCelda/discussions/206): condiciones de envío de la guía, el caso completo.
- [#213](https://github.com/mmasias/pyCelda/discussions/213): retrospectiva de #206 y cambio de método.
- [#92](https://github.com/mmasias/pyCelda/discussions/92): métricas del proyecto por disciplina RUP y coste de los retrocesos.
- [#112](https://github.com/mmasias/pyCelda/discussions/112): agilidad como consecuencia del rigor previo.
- [#842](https://github.com/mmasias/pyCelda/issues/842) y [#849](https://github.com/mmasias/pyCelda/issues/849): los dos defectos que el método no evitó.
- [MVCHowTo](MVCHowTo.md): dónde vive cada regla de negocio en el código.
