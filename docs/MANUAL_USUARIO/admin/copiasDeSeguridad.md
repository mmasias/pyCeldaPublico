<div align=right>

<sub>[Manual de Admin](README.md)</sub>

</div>

# Copias de seguridad

## Qué es

La pantalla donde se ven las copias de seguridad de la base de datos y se gestionan: hacer una copia a demanda, comprobar su salud y, en caso de necesidad, restaurar una. Las copias diarias se siguen generando automáticamente; desde aquí se pueden añadir copias puntuales y consultarlas todas.

## Cómo llegar

Pulsar **💾 Copias de seguridad** en el panel de administración. Para salir, **Volver al Panel de Administración**.

## Qué muestra

Una tabla con las columnas **Familia**, **Fecha**, **Tamaño**, **Esquema**, **Motivo**, **Salud** y **Restaurar**. Si todavía no hay ninguna copia registrada, la pantalla lo indica.

- **Familia**: **Diario** (las automáticas), **Puntual** (las hechas a demanda) o **Previa a restaurar** (la que el sistema hace solo justo antes de cada restauración).
- **Esquema**: la versión de esquema de la base de datos con la que se hizo la copia, o "—" si no se pudo leer. La versión de esquema vigente (y la de la aplicación) se ve también al pie de la pantalla de entrada: `Versión v0.11.8 · esquema 2`.
- **Salud**: vacía hasta que se pulsa **🩺 Comprobar salud de las copias** (ver más abajo).

Por defecto solo se listan las copias **restaurables**: las que existen en el volumen y tienen exactamente la misma versión de esquema que la base de datos actual. Encima de la tabla, la casilla **Mostrar todos (incluye no restaurables)** muestra el historial completo; no borra nada, es solo un filtro visual. Un texto indica cuántas se muestran ("Mostrando X de Y copias"); si ninguna es restaurable, la pantalla lo dice y sugiere activar la casilla.

## Hacer una copia ahora

1. Pulsar **📦 Hacer copia de seguridad ahora**.
2. Escribir, si se quiere, un **Motivo (opcional)**.
3. Pulsar **Crear** (o **Cancelar**).

Se crea una copia de la base de datos actual, de familia **Puntual**; no modifica nada y aparece en la tabla al terminar.

## Comprobar la salud de las copias

Pulsar **🩺 Comprobar salud de las copias**. Revisa cada copia y rellena la columna **Salud** con **Correcta**, **Dañada**, **Ilegible** o **No disponible**, y sobre la tabla aparece el resumen ("N correctas, N dañadas, N ilegibles, N no disponibles"). Al pasar el ratón por una copia dañada se ve el primer mensaje del informe de SQLite. El resultado solo se muestra en pantalla: no se guarda y hay que repetir la comprobación en cada visita. Si hay copias dañadas o ilegibles ocultas por el filtro, el resumen lo advierte; activar **Mostrar todos** para verlas.

## Restaurar una copia

Restaurar **sobrescribe la base de datos viva** con el contenido de la copia y es irreversible para todo lo que se haya hecho después de ella. No es una operación para usar a la ligera: solo ante una pérdida o corrupción de datos real.

1. En la fila de la copia, pulsar **Restaurar**. El botón está desactivado en las copias no restaurables; al pasar el ratón por encima indica el motivo ("Copia no disponible en el volumen", "Versión de esquema ilegible" o "Esquema incompatible con la versión actual").
2. La pantalla avisa de lo que va a ocurrir y pide **escribir el nombre exacto del archivo** de la copia. Hasta que coincida, el botón **Restaurar** de la confirmación permanece desactivado. **Cancelar** abandona sin cambios.
3. Pulsar **Restaurar** para confirmar.

Salvaguardas del sistema:

- **Copia previa automática**: antes de tocar nada, se hace una copia de la base de datos actual (familia **Previa a restaurar**, con el motivo "antes de restaurar" y el nombre del fichero). Así queda siempre un punto de vuelta atrás.
- **Rechazo por esquema incompatible**: si la copia no tiene la misma versión de esquema que la base de datos actual, la restauración se rechaza y se indica ambas versiones.
- **Rechazo por integridad**: antes de restaurar se comprueba la integridad del fichero; si la copia está dañada, se rechaza con un mensaje de error y no se cambia nada.

Si todo es correcto, aparece "Restauración en curso" y el sistema se reinicia en unos segundos: hay que recargar la página pasados 30 segundos.

---

<div align=center>

| [Seguimiento de guías](seguimientoDeGuias.md) | [Índice](README.md) | [Cursos académicos](cursosAcademicos.md) |
|---|:-:|---|

</div>
