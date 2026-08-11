<div align=right>

<sub>**Home** / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub>

</div>

# pyCelda -- subconjunto público

Subconjunto público de **pyCelda**, sistema de gestión de guías docentes universitarias modelado con RUP. Este repo expone la capa de **Requisitos**: actores y casos de uso, el catálogo detallado de los 91 casos de uso (especificación + wireframe de cada uno) y el mockup navegable por actor derivado de ambos.

No incluye modelo de dominio, fases de Análisis/Diseño ni datos reales de la institución (nombres/emails de profesorado) -- esas partes viven en el repo de trabajo privado.

## Navegación

- **[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md)** -- diagramas de actores y diagrama de contexto (estados de disponibilidad de casos de uso) por actor: `Admin`, `DirectorGrado`, `Profesor`.
- **[Detalle de casos de uso](/RUP/01-requisitos/03-detalle-casos-uso/README.md)** -- una carpeta por caso de uso (91 en total), con su statechart de especificación y su wireframe.
- **[Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)** -- el catálogo anterior recorrido como prototipo clicable, una página por caso de uso con su wireframe y la tabla de botones que lleva al siguiente. Punto de entrada por actor: [Admin](/docs/PROPUESTA_WIREFRAME/admin/iniciarSesion.md) / [DirectorGrado](/docs/PROPUESTA_WIREFRAME/directorGrado/iniciarSesion.md) / [Profesor](/docs/PROPUESTA_WIREFRAME/profesor/iniciarSesion.md).

## Cómo se generan los mockups

[`docs/scripts/generar_mockup_navegable.py`](/docs/scripts/generar_mockup_navegable.py) deriva cada página del mockup a partir del diagrama de contexto del actor más los wireframes disponibles en el catálogo de detalle -- no se escribe a mano. Detalle completo del mecanismo en el [README de mockups](/docs/PROPUESTA_WIREFRAME/README.md).

## Citas al repo de trabajo

Varias fichas de caso de uso referencian discussions/issues del repo privado (`github.com/mmasias/pyCelda`) donde se debatió la decisión de modelado correspondiente. Son citas de procedencia, no enlaces navegables para quien no tenga acceso a ese repo -- el texto que las acompaña ya explica la decisión sin necesidad de abrirlas.
