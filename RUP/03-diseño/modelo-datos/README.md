<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# Modelo de datos

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-09-01
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Vista **relacional** del almacén de datos (SQLite + SQLAlchemy, 26 tablas), complemento del [diagrama de clases de diseño](/RUP/03-diseño/diagrama-clases-diseño.puml) (vista OO, Fat Model). Peldaño intermedio de la escala de tres representaciones del sistema (discussion [#59](https://github.com/mmasias/pyCelda/discussions/59)): un nivel por debajo de las clases de diseño, comprometido con el esquema físico.

La vista OO deja invisibles las 6 tablas de unión (son `secondary=` de una relación), las columnas FK reales y su nulabilidad, y qué asociación del dominio es FK física y cuál lógica. Este artefacto las documenta. Criterio de arranque en la discussion [#196](https://github.com/mmasias/pyCelda/discussions/196).

## Artefactos

| Fichero | Qué es |
|---|---|
| [`DER.puml`](DER.puml) | Diagrama entidad-relación en notación relacional (notación de [pySigHor](https://github.com/mmasias/pySigHor/blob/diseño-fastapi-react/RUP/02-diseño/DER.puml): `class` con `<<PK>>`/`<<FK>>`/`<<PK,FK>>`, crow's foot). Un solo diagrama, con los 3 `package` del modelo de dominio. **100% generado.** |
| [`diccionario-datos.md`](diccionario-datos.md) | Sección por tabla (columnas, tipos, nulabilidad, defaults, claves) **generada**, más una **capa de intención de diseño a mano** (dominios de enum, FK lógica vs física, denormalizaciones, reglas de consistencia). |

<div align=center>

|![](/images/RUP/03-diseño/modelo-datos/DER.svg)|
|-|
|<div align=right><sup>Código fuente: [DER.puml](DER.puml)</sup></div>|

</div>

## Enfoque híbrido: generado + capa de intención a mano

Los hechos estructurales (tablas, columnas, tipos, nulabilidad, defaults, PK, FK, unique) se **generan** por introspección de `SQLAlchemy.metadata` -- no se transcriben a mano, no driftean. Ya hay tres representaciones del dominio (modelo de dominio, clases de análisis, clases de diseño) más el código; un cuarto artefacto 100% a mano se pudre (el PR [#192](https://github.com/mmasias/pyCelda/pull/192) lo demostró: el `diagrama-clases-diseño.puml` tenía `actualizar()` ausente en dos repositorios).

Pero un artefacto 100% generado no captura lo que SQLAlchemy no sabe: que `String(20)` en `guias.estado` es el dominio `{Borrador, EnRevision, Aprobada, Rechazada}`, que `guias.grado_id` es denormalizado sin FK, que `(Grado, Asignatura)` es único aunque no haya `UniqueConstraint`. Eso se escribe **a mano**, referenciando el [README del modelo de dominio](/RUP/00-modelo-del-dominio/README.md) en vez de duplicar el "por qué".

### Delimitación de las dos capas

- **`DER.puml`**: 100% generado. Su "por qué" (reparto en `package`, etiquetas de relación, notas) vive como **constantes Python curadas** en `backend/app/scripts/generar_modelo_datos.py` (`PAQUETES`, `ETIQUETAS_REL`, `NOTAS_DER`), revisadas en el PR. Regenerar reescribe el fichero entero -- no hay prosa en el output que pisar.
- **`diccionario-datos.md`**: la capa estructural va entre `<!-- BEGIN GENERADO -->` y `<!-- END GENERADO -->`; el generador solo reescribe esa región. La capa de intención (todo lo anterior a los marcadores) es prosa a mano y no se toca nunca. Las columnas `dominio` y `nota` de las tablas generadas se rellenan desde constantes curadas del script (`DOMINIOS`, `NOTAS_COLUMNA`).

## Generador

`backend/app/scripts/generar_modelo_datos.py`:

```
python -m app.scripts.generar_modelo_datos           # escribe DER.puml + región del .md
python -m app.scripts.generar_modelo_datos --check    # exit 1 si hay drift
```

No necesita base de datos: importa `app.models` (registra las tablas en `Base.metadata`) e introspecciona. Idempotente.

## Regla de mantenimiento

Un PR que toca `backend/app/models/` **regenera el DER y el diccionario y revisa la capa de intención** -- misma clase de obligación que actualizar el README del modelo de dominio. `generar_modelo_datos.py --check` en verde es la comprobación. La regeneración del **SVG** de `images/` es un paso aparte (mismo criterio que el resto de SVG del repo).

## Referencias

- [Discussion #196](https://github.com/mmasias/pyCelda/discussions/196) -- criterio de este artefacto.
- [Diagrama de clases de diseño](/RUP/03-diseño/diagrama-clases-diseño.puml) -- vista OO complementaria.
- [README del modelo de dominio](/RUP/00-modelo-del-dominio/README.md) -- el "por qué" de cada regla, no reexplicado aquí.
- [Issue #181](https://github.com/mmasias/pyCelda/issues/181) -- `AsignaturaGrado.asignatura_id`, FK física hacia `Asignatura` (nullable, cerrado 2026-09-05).
