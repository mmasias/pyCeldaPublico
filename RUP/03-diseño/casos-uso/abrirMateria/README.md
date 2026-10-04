<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirMateria() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirMateria/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirMateria/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.2
- **Fecha**: 2026-08-25
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`abrirMateria()`](/RUP/02-analisis/casos-uso/abrirMateria/README.md), en sus dos variantes. La `DirectorPrograma` presenta el detalle de la `Materia` fusionando tres colecciones asociadas -- `MetodologiaDocente` (vía `MetodologiaMateria`), `ResultadoAprendizaje` y `AsignaturaPrograma` -- agregación de lectura con cuatro consultas, mismo mecanismo que `abrirGuia()`. La `Admin` presenta las mismas tres colecciones en solo lectura: ve el dato, no lo gestiona (asociar/quitar/editar sigue siendo de `DirectorPrograma`). Construida en el lote de Materia/AsignaturaPrograma junto a `crearMateria()`/`editarMateria()`.

**Corrección v1.2**: la variante Admin se definió originalmente como reducida (solo `AsignaturaPrograma`) razonando que las secciones de asociación "no tienen sentido sin los botones de DirectorPrograma" -- eso mezclaba quién actúa con quién ve el dato. Ahora expone las tres colecciones; el diagrama `secuencia-admin.svg` conserva las dos consultas originales y omite las dos nuevas (copia literal de las de la variante DirectorPrograma), sin rehacerse.

Este `secuencia.puml` contiene **dos diagramas**: el primero (`abrirMateria-diseño`) es la variante `DirectorPrograma`; el segundo (`abrirMateria-admin-diseño`) es la variante `Admin` -- mismo criterio de troceo que `secuencia.puml` de `iniciarSesion()` y de la variante Admin de [`abrirProgramas()`](../abrirProgramas/README.md).

## Diagrama de secuencia de diseño

<div align=center>

|`DirectorPrograma` (`/api/v1/materias/{materia_id}`)|`Admin` reducida (`/api/v1/admin/materias/{materia_id}`)|
|:-:|:-:|
|![](/images/RUP/03-diseño/casos-uso/abrirMateria/secuencia.svg)|![](/images/RUP/03-diseño/casos-uso/abrirMateria/secuencia-admin.svg)|
|<sup>Código fuente: [secuencia.puml](secuencia.puml)</sup>|<sup>mismo fichero, segundo bloque `@startuml`</sup>|

</div>

## Participantes

### Variante DirectorPrograma

- **Vista**: `AbrirMateriaView` (React) -- pide `GET /api/v1/materias/{materia_id}`; presenta `nombre`, las `MetodologiaDocente` asociadas (con `descripcion_propia`), los `ResultadoAprendizaje` asociados y las `AsignaturaPrograma` de la `Materia`.
- **API**: `routers/materia.py::obtener_materia(materia_id)` -- función suelta; guard de `DirectorPrograma`.
- **Modelo**: ninguno con lógica propia invocada -- `Materia`, `MetodologiaMateria`, `ResultadoAprendizaje` y `AsignaturaPrograma` portan los datos presentados.
- **Repositorio**: `MateriaRepository.obtener(materia_id)` / `.listar_resultados_aprendizaje_de(materia_id)`; `MetodologiaMateriaRepository.listar_de(materia_id)`; `AsignaturaProgramaRepository.listar_de_la_materia(materia_id)`.

### Variante Admin (solo lectura)

- **Vista**: `MateriaAdmin.tsx` (React, ruta `/admin/materias/{materia_id}`) -- pide `GET /api/v1/admin/materias/{materia_id}`; presenta `nombre` y las tres colecciones en tablas de solo lectura: "Metodologías docentes asociadas" (código, descripción, descripción propia), "Resultados de aprendizaje asociados" (código, tipo) y "Asignaturas de esta materia" (asignatura, curso, carácter, `[Abrir]` deshabilitado en esta rebanada), con botones `[Editar]` (a `EditarMateriaAdmin.tsx`) y `[Volver al listado]`. Sin botones de asociación ni `[Quitar]`: esas acciones son de `DirectorPrograma`.
- **API**: `routers/materia.py::obtener_materia_admin(materia_id)` -- función nueva; guard `Depends(require_admin)`; el sufijo `_admin` evita colisionar con `obtener_materia()`.
- **Modelo**: ninguno con lógica propia invocada -- `Materia`, `MetodologiaMateria`, `ResultadoAprendizaje` y `AsignaturaPrograma` portan los datos presentados.
- **Repositorio**: `MateriaRepository.obtener(materia_id)` / `.listar_resultados_aprendizaje_de(materia_id)`; `MetodologiaMateriaRepository.listar_de(materia_id)`; `AsignaturaProgramaRepository.listar_de_la_materia(materia_id)` -- los cuatro reutilizados tal cual de la variante DirectorPrograma.

## Decisiones de diseño

- **`MateriaAdminDetalleResponse`, response propio en vez de reusar `MateriaDetalleResponse`**: desde v1.2 ambas variantes exponen las mismas tres colecciones y difieren solo en el namespace de autorización; se mantienen como dos responses explícitos porque su evolución es independiente (la variante Admin podría ganar campos propios, p. ej. `estado` de borrado lógico).
- **Cuatro lecturas, una por colaboración de Análisis** -- copia literal de las consultas de la variante DirectorPrograma.
- **Namespace `/api/v1/admin/materias/{materia_id}` con `Depends(require_admin)`** -- separado del de `DirectorPrograma`, mismo criterio del resto del namespace Admin.
- **Admin ve el dato, no lo gestiona**: las tablas de metodologías/resultados no llevan `[Editar]`/`[Quitar]` ni botón `+ Asociar` -- quién actúa (`DirectorPrograma`) no determina quién ve (`Admin`), mismo criterio que el `[Abrir]` deshabilitado de la tabla de `AsignaturaPrograma`.
- **La tabla embebida lleva `[Abrir]` deshabilitado**: la variante Admin de `abrirAsignaturaPrograma()` no se construye en esta rebanada; el botón se renderiza con `title="Fuera de alcance de esta rebanada"`.
- **`404` si el identificador no existe** -- guardia de Router sobre el `None` del repositorio.

## Referencias

- [`abrirMateria()` en Análisis](/RUP/02-analisis/casos-uso/abrirMateria/README.md) -- diagrama de colaboración origen, con ambas variantes.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirMateria/README.md) -- fuente compartida; las secciones de asociación son de `DirectorPrograma`.
- [`abrirGuia()` en Diseño](/RUP/03-diseño/casos-uso/abrirGuia/README.md) -- precedente del agregado de lectura por colaboraciones.
- [`abrirMaterias()` en Diseño](/RUP/03-diseño/casos-uso/abrirMaterias/README.md) -- listado del que se alcanza, con su variante Admin construida en este mismo lote.
- [`editarMateria()` en Diseño](/RUP/03-diseño/casos-uso/editarMateria/README.md) -- acción `[Editar]` de esta ficha, construida en este mismo lote.
- [`editarActividadesFormativasMateria()` en Diseño](/RUP/03-diseño/casos-uso/editarActividadesFormativasMateria/README.md) / [`consultarEstadoActividadesFormativasMateria()` en Diseño](/RUP/03-diseño/casos-uso/consultarEstadoActividadesFormativasMateria/README.md) -- el clúster de `ActividadFormativa` (discussion [#227](https://github.com/mmasias/pyCelda/discussions/227)) suma la sección "Actividades formativas de la materia" a la variante `DirectorPrograma` de esta pantalla (rejilla + medidor); `MateriaDetalleResponse` gana el campo al construir el clúster, con audit del agregado `Materia`.
