# Scripts de utilidad

Subconjunto público: solo se incluye `generar_mockup_navegable.py`. El repo de trabajo privado tiene además un extractor que alimenta el catálogo con datos reales de la institución -- fuera del alcance de este repo.

## generar_mockup_navegable.py

Genera el mockup navegable por actor a partir del diagrama de contexto + wireframes SVG disponibles en el catálogo de detalle. Cada página es un CU con su wireframe centrado y una tabla de acciones que mapea cada botón a un CU destino. Véase [`docs/PROPUESTA_WIREFRAME/README.md`](/docs/PROPUESTA_WIREFRAME/README.md) para la definición del artefacto y su valor metodológico.

### Uso

```bash
python3 docs/scripts/generar_mockup_navegable.py <Actor>
# Actor: Admin | Profesor | DirectorGrado (debe existir diagramaContexto<Actor>.puml)
```

### Salida

`docs/PROPUESTA_WIREFRAME/<actor>/<cu>.md` por cada CU detallado del actor (con `wireframe.svg` disponible), más un placeholder por cada estado cuyo CU canónico de entrada no esté detallado.

### Tres tipos de página

| Tipo | Cómo se produce | Cómo se identifica |
|---|---|---|
| Generada | Diagrama + SVG disponible | Sin marca especial |
| Placeholder | CU canónico sin detallar | Texto *Pendiente de detallar: `<CU>()`* donde iría el SVG |
| Override manual | Edición humana con marca | Comentario `<!-- MANUAL OVERRIDE -->` en cualquier línea del fichero |

### Protección de overrides manuales

Cuando una página requiere contenido que el script no sabe producir (botones visibles sin enlace para distinguir permisos de deuda, ajustes de etiquetado, etc.), el editor manual añade la línea:

```
<!-- MANUAL OVERRIDE: el script no sobreescribe este fichero -->
```

en cualquier posición del fichero. El script detecta la marca y **skip** esa página al regenerar, con aviso explícito:

```
[SKIP] abrirAsignaturaGrado.md (override manual protegido)
```

Cualquier otra página del mismo actor se regenera normalmente. Para retirar la protección, basta con borrar la línea del comentario.

### Tres tipos de celda CdU en las tablas

Cada página generada contiene una tabla `|Acción|CdU|`. La celda CdU admite tres formas distinguibles, cada una comunica una razón distinta al lector:

| Tipo | Forma | Significado |
|---|---|---|
| Enlace | `[**Label**](cu.md)` con `<sub>cu()</sub>` | El actor tiene permiso y el CU destino está detallado. Navegación activa. |
| Pendiente | `**Label**` con `<sub>cu()</sub> (pendiente)` | El actor tiene permiso (la transición está en el diagrama) pero el CU no tiene `wireframe.svg` generado. Deuda de catalogación. |
| Vacía | `**Label**` con celda CdU vacía | El actor ve el botón en la interfaz pero no tiene permiso (la transición no está en el diagrama del actor). Restricción por rol. |

La distinción entre `pendiente` y vacía es informativa: comunica al lector del mockup por qué no hay navegación desde ese botón — deuda de catalogación frente a restricción de permisos. El script produce solo las dos primeras (`enlace` y `pendiente`); la celda vacía solo aparece en overrides manuales, donde el editor ha contrastado el wireframe con el diagrama del actor.
