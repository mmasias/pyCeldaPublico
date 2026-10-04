<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/importarActividadesFormativasDeAsignaturaProgramaPrima/README.md) / [Diseño](/RUP/03-diseño/casos-uso/importarActividadesFormativasDeAsignaturaProgramaPrima/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > importarActividadesFormativasDeAsignaturaProgramaPrima()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/importarActividadesFormativasDeAsignaturaProgramaPrima/README.md)|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/importarActividadesFormativasDeAsignaturaProgramaPrima/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/importarActividadesFormativasDeAsignaturaProgramaPrima/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorPrograma`|
|**Objetivo**|Reemplazar el reparto de actividades formativas de una `AsignaturaPrograma` con el de otra `AsignaturaPrograma` prima|
|**Tipo**|Primario|
|**Nivel**|Objetivo de usuario|

</div>

Actor y capa (L6) de [`editarActividadesFormativasAsignaturaPrograma()`](../editarActividadesFormativasAsignaturaPrograma/README.md): self-loop de `ASIGNATURA_PROGRAMA_ABIERTO`. Sin herencia por `Profesor` (a diferencia de la familia `importar*DeGuiaHermana`, donde `DirectorPrograma --|> Profesor`): aquí no hay actor `Profesor` en el flujo.

**`AsignaturaPrograma` prima** (issue [#529](https://github.com/mmasias/pyCelda/issues/529)): otra `AsignaturaPrograma` que comparte `materia_id` con la destino y, por tanto, también `Programa` (`Materia.programa_id` lo fija). No es la relación *hermana* de [`importarBibliografiaDeGuiaHermana()`](../importarBibliografiaDeGuiaHermana/README.md) (mismo `Asignatura` del catálogo, cualquier `Materia`/`Programa`): el criterio aquí es de contenedor, no de catálogo.

**Origen**: una prima **configurada**, es decir, con alguna de sus 10 filas con `horas > 0`. Una prima con las 10 filas a 0 no aporta nada y no se ofrece. Las candidatas se ordenan por proximidad de créditos con la destino (`abs(ects_prima - ects_destino)` ascendente; empate por nombre) y cada una muestra `nombre`, `ects` y `total_horas`; los créditos de la destino se muestran junto a los de cada candidata. Si no hay ninguna, el `<<choice>>` de la especificación lleva a un estado vacío sin botón activo.

**Copia con reemplazo total, real e inmediata**: las 10 filas `ActividadFormativaAsignaturaPrograma` de la destino (siempre presentes, autopobladas) se actualizan **in place** con las `horas` y `porcentaje_presencialidad` de las de la prima origen -- no se borra y recrea. Es exactamente lo que hace `editarActividadesFormativasAsignaturaPrograma()`, solo que los valores vienen copiados en vez de tecleados. Un solo commit. Se pide confirmación antes de ejecutar, porque reemplaza lo que el `DirectorPrograma` ya hubiera tecleado.

**Sin efectos colaterales**: igual que el PUT de edición, no toca el estado de ninguna `Guia`. Sin `HistorialCambio` (atado a `Guia.id`; `AsignaturaPrograma` no tiene auditoría de este tipo). `AsignaturaPrograma` es plantilla persistente sin dimensión de `CursoAcademico`: no hay que resolver curso activo.

**Autorización**: la destino se verifica con la misma comprobación de "dirige" que el resto de endpoints de la `AsignaturaPrograma`; el origen debe estar entre las primas configuradas de esa destino, y si no, 404 uniforme (evita IDOR; la pertenencia de prima ya garantiza el mismo `Programa`).

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `ASIGNATURA_PROGRAMA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO : importarActividadesFormativasDeAsignaturaProgramaPrima()`
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml)
- [`editarActividadesFormativasAsignaturaPrograma()`](../editarActividadesFormativasAsignaturaPrograma/README.md) -- caso de uso hermano cuya operación reutiliza
- [`importarBibliografiaDeGuiaHermana()`](../importarBibliografiaDeGuiaHermana/README.md) -- plantilla de RUP (pantalla de selección real)
- [Issue #529](https://github.com/mmasias/pyCelda/issues/529), [issue #530](https://github.com/mmasias/pyCelda/issues/530)
