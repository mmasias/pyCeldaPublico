<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/restaurarCopiaSeguridad/README.md) / [Diseño](/RUP/03-diseño/casos-uso/restaurarCopiaSeguridad/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > restaurarCopiaSeguridad()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/restaurarCopiaSeguridad/README.md)|[Diseño](/RUP/03-diseño/casos-uso/restaurarCopiaSeguridad/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/restaurarCopiaSeguridad/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/restaurarCopiaSeguridad/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Recuperar la base de datos a un estado anterior sobrescribiéndola con una copia de seguridad del volumen|
|**Tipo**|Primario, de apoyo (soporte a la operación)|
|**Nivel**|Objetivo de usuario|

</div>

**Caso de uso nuevo** (issues [#629](https://github.com/mmasias/pyCelda/issues/629) y [#631](https://github.com/mmasias/pyCelda/issues/631); ampliado por [#677](https://github.com/mmasias/pyCelda/issues/677)/[#679](https://github.com/mmasias/pyCelda/issues/679), [#681](https://github.com/mmasias/pyCelda/issues/681)/[#682](https://github.com/mmasias/pyCelda/issues/682) y [#634](https://github.com/mmasias/pyCelda/issues/634)/[#635](https://github.com/mmasias/pyCelda/issues/635)). Desde `COPIAS_SEGURIDAD_ABIERTO` el `Admin` elige una fila de la tabla, pulsa **Restaurar**, escribe el nombre exacto del archivo y confirma. El `Sistema` valida la copia, guarda una copia previa de la base de datos actual, la sobrescribe y se reinicia.

**Reglas**: la confirmación exige escribir el nombre exacto del archivo (irreversible); solo se restaura una copia que figure en el listado y exista en el volumen; no se restaura una copia dañada ni de esquema distinto al actual (las copias sin marca de versión, valor 0, nunca son restaurables); antes de tocar nada se guarda una copia previa (familia `pre_restauracion`, motivo "antes de restaurar X") que el `Admin` puede volver a restaurar; la auditoría es solo el log del servidor.

**Presentación (reglas que el wireframe no dibuja)**: el botón **Restaurar** de cada fila se deshabilita, con ayuda emergente, si la copia no es restaurable, con tres motivos: "Copia no disponible en el volumen", "Versión de esquema ilegible" o "Esquema incompatible con la versión actual". Por defecto la tabla muestra solo las copias restaurables y el interruptor "Mostrar todos (incluye no restaurables)" muestra el historial completo. El botón de confirmación permanece deshabilitado hasta que el texto escrito coincide exactamente con el nombre del archivo, y cualquier botón Restaurar queda deshabilitado una vez iniciada la restauración.

**Con `<<choice>>`**: las precondiciones sí rechazan. Orden de evaluación en el sistema: (1) copia fuera del listado o ausente del volumen, 404 "Copia de seguridad no encontrada"; (2) copia que no abre como SQLite, 409 "La copia está dañada (integrity_check): no se puede restaurar" más la primera línea del informe si la hay; (3) esquema distinto, 409 "Esquema incompatible: la copia tiene versión X y la base de datos actual Y"; (4) copia que abre pero no pasa la comprobación de integridad, mismo 409 de (2). En todos los rechazos no se escribe nada (ni copia previa ni manifiesto) y el `Admin` sigue en `COPIAS_SEGURIDAD_ABIERTO`.

**Destino de éxito**: el sistema se reinicia, lo que no es un estado del diagrama de contexto. Se modela como retorno a `COPIAS_SEGURIDAD_ABIERTO`: el `Sistema` responde 200 "Restauración en curso. El sistema se reiniciará en unos segundos." antes de apagarse, la pantalla muestra el aviso de recargar en 30 segundos y, tras la recarga, el `Admin` vuelve a la pantalla de copias con la base de datos restaurada. Si la sesión no sobrevive a la restauración, el `Admin` pasa por el login habitual.

## Notas de diseño y trazabilidad

- Orden de comprobaciones y mensajes: ver "Con `<<choice>>`". La comprobación de integridad es la misma que usa [`comprobarCopiasSeguridad()`](../comprobarCopiasSeguridad/README.md): botón y restauración no pueden discrepar.
- El filtro por defecto de solo restaurables (#634/#635) oculta, no borra; el aviso "Mostrar todos" cubre las copias ocultas.
- El frontend decide la restaurabilidad con el `esquema_version` y el `disponible` que devuelve el listado, leídos del propio fichero de cada copia (#679), frente a la versión de esquema de la BD actual, por lo que no detecta una copia dañada: esa la detecta el backend al confirmar (o la comprobación de salud).
- El destino "reinicio" se documenta como `COPIAS_SEGURIDAD_ABIERTO` por no existir un estado de reinicio en el diagrama de contexto.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `COPIAS_SEGURIDAD_ABIERTO --> COPIAS_SEGURIDAD_ABIERTO : restaurarCopiaSeguridad()`
- [`consultarCopiasSeguridad()`](../consultarCopiasSeguridad/README.md) -- pantalla desde la que se pide
- [`comprobarCopiasSeguridad()`](../comprobarCopiasSeguridad/README.md) -- misma comprobación de integridad
- Issues [#629](https://github.com/mmasias/pyCelda/issues/629), [#631](https://github.com/mmasias/pyCelda/issues/631), [#677](https://github.com/mmasias/pyCelda/issues/677), [#679](https://github.com/mmasias/pyCelda/issues/679), [#681](https://github.com/mmasias/pyCelda/issues/681), [#682](https://github.com/mmasias/pyCelda/issues/682), [#634](https://github.com/mmasias/pyCelda/issues/634), [#635](https://github.com/mmasias/pyCelda/issues/635)
