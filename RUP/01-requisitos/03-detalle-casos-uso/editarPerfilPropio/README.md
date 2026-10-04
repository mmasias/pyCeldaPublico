<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/editarPerfilPropio/README.md) / [Diseño](/RUP/03-diseño/casos-uso/editarPerfilPropio/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarPerfilPropio()

> |[🏠️](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarPerfilPropio/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarPerfilPropio/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor` (heredado sin cambios por `DirectorPrograma`, `DirectorPrograma --|> Profesor`)|
|**Objetivo**|Editar el propio perfil académico -- ORCID, doctorado, acreditación y sexenios/quinquenios -- sin pasar por `Admin`|
|**Tipo**|Primario, de apoyo (presentación de credenciales, no afecta al ciclo de la `Guia`)|
|**Nivel**|Objetivo de usuario|

</div>

**Caso de uso nuevo** (issue [#423](https://github.com/mmasias/pyCelda/issues/423)). Manuel: "Gestión de perfil del profesor -- Nombre, apellidos, email, certificaciones, acreditaciones (las que sean pertinentes en España), ORCID y esas menudencias que les gustan (presumir) a los pedagogos". Acotado en el diseño previo: autoservicio (no Admin), campos estructurados fijos (no lista abierta de credenciales), `nombre` se queda como campo único (sin separar apellidos), privado esta tanda (sin mostrarse en la Guía docente ni en listados públicos -- ver [Pendiente](#pendiente)).

**Fuera del modelo por capas L0-L10** -- mismo criterio que [`consultarCopiasSeguridad()`](/RUP/01-requisitos/03-detalle-casos-uso/consultarCopiasSeguridad/README.md): `Profesor` en [`modeloDominio.puml`](/RUP/00-modelo-del-dominio/modeloDominio.puml) solo modela `nombre`/`email` a nivel de Requisitos (el detalle exhaustivo de columnas vive en [Diseño](/RUP/03-diseño/modelo-datos/README.md), no en el diagrama de clases conceptual) -- los 12 atributos nuevos del perfil académico no estaban reservados en ninguna capa previa, no encajan en el modelo bottom-up.

**Un solo CU para ver+editar** -- no se modela como par `abrirX()`/`editarX()` (patrón de `Guia`/`PonderacionEvaluacion`/`ReferenciaBibliografica`/`Sesion`, todos ellos con una pantalla plural que precede al detalle): aquí no hay navegación de lista a registro, se llega directo desde `INICIO_ABIERTO` al propio (único) perfil. Mismo criterio que `consultarCopiasSeguridad()`/`consultarHistorialCambios()`, que combinan lectura + acción en un único CU.

**Doce columnas nuevas en `Profesor`, todas opcionales** (`orcid`, `es_doctor`+`universidad_doctorado`+`anio_doctorado`, `figura_acreditacion`+`organismo_acreditador`+`organismo_acreditador_otro`, `num_sexenios`+`anio_ultimo_sexenio`+`tramitando_sexenio`, `num_quinquenios`+`anio_ultimo_quinquenio`) -- sin backfill posible (dato nunca capturado hasta ahora), mismo criterio que `fecha_creacion` de `Guia` (migrar_fecha_creacion_guia.py).

**Figura de acreditación + organismo acreditador, por separado**: la figura (`AYUDANTE_DOCTOR`/`CONTRATADO_DOCTOR`/`PROFESOR_UNIVERSIDAD_PRIVADA`/`TITULAR_UNIVERSIDAD`/`CATEDRATICO_UNIVERSIDAD`) es una cosa, quién la certifica es otra -- `ANECA` es el organismo estatal, pero las agencias autonómicas (AQU Catalunya, ACSUCYL, ACSUG, DEVA Andalucía, ACPUA Aragón...) emiten acreditaciones igual de válidas. `organismo_acreditador_otro` (texto libre) cuando no es `ANECA`, exigido en servidor si se elige "Otro" -- un `PUT` directo a la API con `organismo_acreditador="OTRO"` y el detalle vacío es rechazado (422), no solo oculto en el formulario.

**Sexenios/quinquenios con año del último y trámite en curso**: además del recuento, el año del último reconocido (limpiado a `None` en servidor si el recuento es 0) y, solo para sexenios, si hay uno en evaluación ahora mismo (`tramitando_sexenio`) -- los quinquenios docentes no tienen ese matiz en España, son administrativos sin evaluación externa competitiva, a diferencia de los sexenios (CNEAI), evaluados por comisión.

**Privado esta tanda**: solo el propio `Profesor` ve/edita su perfil -- no aparece en `abrirGuia()`/`descargarGuiaPDF()`/`previsualizarGuia()` ni en ningún listado de `Admin`/`DirectorPrograma`. Mostrarlo (p.ej. en la sección "Profesorado" de la Guía docente) queda para una iteración futura si se pide -- ver [Pendiente](#pendiente).

## Pendiente

- Visibilidad pública del perfil (Guía docente, listados de `Admin`/`DirectorPrograma`) -- explícitamente fuera de esta tanda, a petición.
- Separar `nombre` en `nombre`/`apellidos` -- descartado en el diseño previo, `nombre` se queda como campo único de texto libre.

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `INICIO_ABIERTO --> editarPerfilPropio --> INICIO_ABIERTO`
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- package "Perfil", `Profesor -- editarPerfilPropio`
- [`consultarCopiasSeguridad()`](/RUP/01-requisitos/03-detalle-casos-uso/consultarCopiasSeguridad/README.md) -- precedente de CU fuera del modelo por capas L0-L10
- [`consultarHistorialCambios()`](/RUP/01-requisitos/03-detalle-casos-uso/consultarHistorialCambios/README.md) -- precedente de CU único que combina lectura + acción sin `abrir()` separado
- Issue [#423](https://github.com/mmasias/pyCelda/issues/423) -- diseño original del CU
