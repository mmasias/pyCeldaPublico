<div align=right>

<sub>[Manual de Profesor](README.md)</sub>

</div>

# Planificación docente y cronograma

## Qué es

El cronograma de sesiones de la asignatura: una lista numerada de las clases previstas, con su tipo y una breve descripción de cada una.

## Cuándo se necesita

Antes de poder enviar la guía a revisión, es necesario alcanzar un número mínimo de sesiones registradas (indicado en la propia pantalla, por ejemplo "mínimo 25"). Ese mínimo lo fija Admin para la asignatura.

## Cómo llegar

Desde la guía, pulsar **🔧 Gestionar planificación docente**, a la derecha del título **Planificación docente**.

## Qué muestra

Una tabla numerada con cada sesión: **#**, **Tipo** y **Descripción**. Las filas se colorean según el tipo de clase (teórica, práctica o teórico/práctica) para identificarlas de un vistazo; hay una leyenda encima de la tabla. Debajo, un aviso con el total de sesiones y el mínimo exigido, en rojo si todavía no se alcanza.

## Crear una sesión

1. Pulsar **➕ Añadir fila**. Se añade una fila vacía al final de la tabla.
2. Elegir el **Tipo**: Clase Teórica, Clase Práctica, Clase Teórico/Práctica, Clase Laboratorio, Evaluación Continua o Evaluación Parcial.
3. Escribir una **Descripción** breve de lo que se trabaja en esa sesión.

La fila se guarda sola en cuanto la descripción deja de estar vacía y se pasa a otro campo -- no hay un botón "Guardar" aparte, y mientras se guarda aparece el aviso "Guardando...". **➕ Añadir fila** puede pulsarse varias veces seguidas para preparar varias sesiones sin salir de la pantalla; una fila todavía vacía puede descartarse con **➖** (Quitar) antes de completarla.

## Límite de la descripción

La descripción de cada sesión admite un máximo de **500 caracteres**. Si se supera, se rechaza con el mensaje "La descripción de la sesión supera el límite de 500 caracteres" y la sesión no se guarda.

## Editar o eliminar una sesión

Cambiar el tipo o la descripción directamente en la fila de la tabla guarda el cambio al pasar a otro campo, igual que al crear una sesión. Pulsar la papelera **🗑️** (Eliminar) dos veces seguidas (la segunda, cuando dice "pulsa de nuevo para confirmar") para quitar la sesión de la vista -- el borrado no se hace definitivo hasta guardar el borrador de la guía, igual que con los instrumentos de evaluación y la bibliografía.

Si un guardado falla (por ejemplo, por un corte de red), aparece un mensaje de error con el botón **Reintentar**; lo escrito no se pierde.

## Duplicar una sesión

Pulsar **📑 Duplicar** en la fila de una sesión crea una copia con el mismo tipo y la misma descripción, justo debajo de la original -- las sesiones que venían después se renumeran automáticamente para dejar sitio a la copia. Si falla, aparece el mismo tipo de aviso con el botón **Reintentar**.

Pensado para sesiones consecutivas parecidas -- un tema que continúa, una práctica que se repite -- editando después solo lo que cambia en vez de escribir la sesión entera de nuevo.

## Arrancar la planificación de golpe

Si la guía todavía no tiene ninguna sesión creada, aparece el botón **Crear N sesiones genéricas** (N es el mínimo exigido para la asignatura). Es un atajo para no partir de una tabla completamente vacía.

1. Pulsar **Crear N sesiones genéricas**.
2. El botón cambia a **Crear N sesiones genéricas (pulsa de nuevo para confirmar)**. Pulsarlo otra vez confirma la creación; **Cancelar** la descarta.

Esto crea de golpe N sesiones de Clase Teórica, sin descripción, numeradas de la 1 a la N, ya guardadas -- no hace falta pulsar **💾 Guardar borrador** después. A partir de ahí, cada una puede editarse para ajustar el tipo y añadir la descripción real de la clase. El botón solo está disponible mientras la planificación está completamente vacía: en cuanto existe al menos una sesión (aunque sea creada a mano), desaparece.

## Importar de una asignatura hermana

Igual que con la bibliografía: si la asignatura se imparte también en otro programa y esa guía ya está aprobada, la planificación docente completa puede copiarse directamente.

1. Pulsar **Importar de asignatura hermana** (solo aparece si hay alguna guía de la que importar).
2. En **Importar desde**, elegir la guía de origen. Cada opción muestra el programa, el código de la asignatura, la fecha en que se aprobó y cuántas sesiones tiene.
3. Aparece un aviso: la importación reemplaza por completo la planificación actual de la guía, incluida cualquier sesión añadida a mano, y las sesiones importadas se renumeran de 1 en adelante. Si la guía de origen no tiene ninguna sesión, el aviso lo indica explícitamente.
4. Pulsar **Importar planificación docente** para confirmar, o **Cancelar** para volver atrás sin cambiar nada.

Como con la bibliografía, importar sustituye la planificación de inmediato -- no hace falta guardar el borrador después.

## Importar desde texto

Alternativa a la importación de una asignatura hermana cuando la planificación ya existe como texto (un documento, un correo): se pega y pyCelda crea las sesiones.

1. Pulsar **Importar desde texto**.
2. Pegar en el cuadro de texto una sesión por línea, con el formato `CODIGO - Descripción`. El separador es el primer ` - ` (espacio, guion, espacio) de la línea; los ` - ` posteriores forman parte de la descripción.
3. Pulsar **Importar planificación docente** para confirmar, o **Cancelar** para volver atrás sin cambiar nada.

El código (mayúsculas o minúsculas, da igual) fija el tipo de la sesión:

| Código | Tipo de sesión |
|---|---|
| `CT` | Clase teórica |
| `CP` | Clase práctica |
| `CTP` | Clase teórico-práctica |
| `CL` | Clase laboratorio |
| `EC` | Evaluación continua |
| `EP` | Evaluación parcial |

Reglas de lectura del texto -- ninguna línea se rechaza por su código ni por estar vacía:

- Las líneas vacías se ignoran.
- Una línea cuyo código no se reconoce se importa como clase teórica, con la línea completa como descripción.
- Una línea con un código reconocido pero sin contenido (`CTP -`, `CTP-` o `CTP` sola) se importa con ese tipo y la descripción vacía.

La pantalla avisa de que la importación reemplaza por completo la planificación actual de la guía, incluida cualquier sesión añadida a mano, e indica cuántas sesiones se sustituyen; las sesiones importadas se renumeran de 1 en adelante. Una línea cuya descripción supera los 500 caracteres sí rechaza la importación entera: aparece "Línea N: la descripción supera el límite de 500 caracteres" (N cuenta también las líneas vacías del texto pegado), no se borra nada y no se recorta en silencio. Lo mismo ocurre al importar de una asignatura hermana si alguna sesión de origen supera el límite ("Sesión N: ..."). Si el texto está vacío, la planificación queda vacía y la pantalla lo advierte. Como en la importación de una hermana, el cambio es inmediato -- no hace falta guardar el borrador después -- y el mínimo de sesiones exigido para la asignatura no se modifica. Si la guía estaba **Aprobada**, pasa a **Borrador**.

## Volver

**Volver a la Guía**, arriba a la derecha, lleva de vuelta a la guía docente; **🏠 Inicio** vuelve a la lista de guías.

---

<div align=center>

| [Referencias bibliográficas](referenciasBibliograficas.md) | [Índice](README.md) | [Enviar, previsualizar y descargar](enviarPrevisualizarYDescargar.md) |
|---|:-:|---|

</div>
