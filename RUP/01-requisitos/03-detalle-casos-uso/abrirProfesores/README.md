<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirProfesores()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirProfesores/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirProfesores/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Consultar el listado de `Profesor` del catálogo institucional|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

**Columna "Asignaturas" (issue [#310](https://github.com/mmasias/pyCelda/issues/310))**: número de `AsignaturaGrado` que imparte cada `Profesor` hoy, junto a Nombre/Email -- antes solo se veía entrando profesor a profesor (`ProfesorRepository.asignaturas_impartidas()`, en la ficha de detalle). No es columna propia de `Profesor`: recuento en vivo vía `asignaturas_grado_profesores`, una sola consulta agregada (`GROUP BY profesor_id`) para todo el listado, no un bucle por profesor -- sin migración. No CU nuevo: mismo tratamiento de columna añadida a un listado ya existente que la "Descripción" de `PonderacionesEvaluacion` (issue [#279](https://github.com/mmasias/pyCelda/issues/279)) o el "Cuatrimestre" de `TablaMisGuias` (issue [#291](https://github.com/mmasias/pyCelda/issues/291)).

**Nombre y Email fusionados en una columna "Profesor" (issue [#312](https://github.com/mmasias/pyCelda/issues/312))**: nombre en línea principal, email debajo con `className="nota"` (clase ya existente, `font-size: 0.875rem; color: #6b7280` -- misma que "Última actualización" de [`ListaGuiasDelGrado.tsx`](/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoGuias/README.md), sin CSS nuevo). Se descartó nombre-como-enlace `mailto:` en la reflexión con Manuel -- patrón sin precedente en el proyecto (cero `<a>`/`mailto:`/`<Link>` en todo el frontend, la navegación siempre es un botón explícito). Caso `nombre === null` (filas del seed sin backfillear): la línea principal cae al email, sin repetirlo en una segunda línea `.nota`. Columnas resultantes: **Profesor | Asignaturas | (Abrir) | (Eliminar)**. Tabla en jerarquía de texto (`className="jerarquica"`, patrón de [#283](https://github.com/mmasias/pyCelda/issues/283)): `Profesor` a tamaño base (el email va en su propio `.nota` interno, ya secundario por diseño), `Asignaturas`/botones un punto menos.

**Nota no bloqueante -- `CursoAcademico` (issue [#222](https://github.com/mmasias/pyCelda/issues/222), sin construir aún)**: `asignaturas_grado_profesores` es la asociación *en vivo actual*, sin noción de curso académico -- hoy el recuento es correcto porque no existe otra cosa que contar (una `AsignaturaGrado` no tiene historial por curso, solo el estado presente). Cuando `CursoAcademico` se modele de verdad, este recuento debería acotarse al curso vigente, no sumar todo el histórico de asignación -- de lo contrario un profesor que dejó de impartir una asignatura hace dos cursos seguiría contando aquí. Dejado por escrito para cuando llegue #222; no se toca nada de esto ahora.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SISTEMA_DISPONIBLE --> PROFESORES_ABIERTO : abrirProfesores()`
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` sobre `Profesor`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Profesor -u-|> Actor`, catálogo independiente
- Datos reales: [`backend/app/data/seed/profesores.json`](/backend/app/data/seed/profesores.json) (repo privado)
- Issue [#310](https://github.com/mmasias/pyCelda/issues/310) -- origen de la columna "Asignaturas"
- Issue [#312](https://github.com/mmasias/pyCelda/issues/312) -- origen de la fusión Nombre+Email en "Profesor"
- Issue [#222](https://github.com/mmasias/pyCelda/issues/222) -- `CursoAcademico`, motivo de la nota no bloqueante de arriba
