<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarReferenciaBibliografica()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarReferenciaBibliografica/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/eliminarReferenciaBibliografica/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`eliminarReferenciaBibliografica()`](/RUP/01-requisitos/03-detalle-casos-uso/eliminarReferenciaBibliografica/README.md): confirmación simple, sin `<<choice>>` (nada depende estructuralmente de una `ReferenciaBibliografica`). Su único efecto es quitar el ítem de la **lista de trabajo de la sesión** -- la misma lista que `abrirReferenciasBibliograficas()`/`abrirGuia()` construyen por fusión vinculado+pendiente, y que [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) recibirá completa al guardar. **No toca la fila de `ReferenciaBibliografica`** -- no la borra, no la edita, ningún repositorio de esa entidad interviene aquí -- y **no toca `Guia`**. Mismo criterio que [`eliminarPonderacionEvaluacion()`](../eliminarPonderacionEvaluacion/README.md): sin ninguna clase de Modelo en su diagrama de colaboración, solo Vista y Controlador -- no hay ninguna entidad de dominio involucrada, "eliminar" significa "excluir de la lista que se enviará a `guardarBorradorGuia()`", que es quien de verdad decide, por ausencia en esa lista, desvincular la fila real.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/eliminarReferenciaBibliografica/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EliminarReferenciaBibliograficaView`

**Responsabilidades:**
- presenta la información de la `ReferenciaBibliografica` (`tipo`, `referencia`) -- datos ya conocidos de la fila del listado que originó la solicitud, sin releer nada.
- presenta la pregunta de confirmación y permite solicitar confirmar o cancelar.
- en la rama verde, quita el ítem de la lista de trabajo de la sesión y presenta la lista actualizada.
- en la rama azul, cierra la confirmación sin tocar la lista.

**Colaboraciones:**
- **Entrada:** `:REFERENCIAS_BIBLIOGRAFICAS_ABIERTO` -- el `Profesor` solicita eliminar una `ReferenciaBibliografica` desde su fila en el listado.
- **Control:** `ReferenciaBibliograficaController`.
- **Salida:** `:REFERENCIAS_BIBLIOGRAFICAS_ABIERTO` en ambos casos -- self-loop, con "quitada de la lista de trabajo" (verde) o "cancelada, sin cambios" (azul).

## Clases de controlador

### `ReferenciaBibliograficaController`

**Responsabilidades:**
- confirma la eliminación (`confirmarEliminacion(referenciaId)`) -- sin validar nada, no hay `<<choice>>` bloqueante ni regla de negocio que comprobar. Mismo controlador que ya usa `crearReferenciaBibliografica()`, no uno nuevo.
- no llama a ningún repositorio ni a `Guia` -- no hay nada que persistir en este caso de uso, la lista de trabajo es responsabilidad de la Vista.

**Colaboraciones:**
- **Entrada:** `EliminarReferenciaBibliograficaView`.
- **Salida:** ninguna.

## Flujo de colaboración principal

1. Desde `:REFERENCIAS_BIBLIOGRAFICAS_ABIERTO`, el `Profesor` solicita eliminar una `ReferenciaBibliografica` desde su fila en el listado -- los datos a presentar viajan con la solicitud, sin releer nada; se abre `EliminarReferenciaBibliograficaView` con la pregunta de confirmación.

### Rama verde (confirmar)

2. El `Profesor` solicita confirmar; la Vista pide al Controlador confirmar la eliminación (`confirmarEliminacion(referenciaId)`); el Controlador no valida nada y confirma. La Vista quita el ítem de la lista de trabajo de la sesión y presenta la lista actualizada; la colaboración termina en `:REFERENCIAS_BIBLIOGRAFICAS_ABIERTO`.

### Rama azul (cancelar)

3. El `Profesor` solicita cancelar; la Vista cierra la confirmación sin tocar la lista de trabajo; la colaboración termina en `:REFERENCIAS_BIBLIOGRAFICAS_ABIERTO`, sin cambios.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/eliminarReferenciaBibliografica/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/eliminarReferenciaBibliografica/wireframes.puml) -- fuente de verdad del patrón confirmar/cancelar sin `<<choice>>`.
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `REFERENCIAS_BIBLIOGRAFICAS_ABIERTO --> REFERENCIAS_BIBLIOGRAFICAS_ABIERTO : eliminarReferenciaBibliografica()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Guia *-- ReferenciaBibliografica`, sin entidad que dependa de ella.
- [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) -- quien recibe la lista de trabajo ya sin este ítem y desvincula la fila real por ausencia (`Guia.sincronizarReferencias()`).
- [`crearReferenciaBibliografica()`](../crearReferenciaBibliografica/README.md) -- mismo `ReferenciaBibliograficaController`, reutilizado aquí.
