# pyCelda

Hola. Esto es **pyCelda**: un sistema para gestionar las guías docentes de una universidad -- el documento que cada profesor rellena cada curso con el contenido, la evaluación y la bibliografía de su asignatura, y que un director de grado revisa y aprueba antes de que se publique.

Este repositorio es un subconjunto público de un proyecto de trabajo más amplio. Aquí puedes hacer dos cosas: **verlo funcionar** y, si te pica la curiosidad, **asomarte a cómo está pensado por dentro**.

## 1. Pruébalo

No hay que instalar nada: es un prototipo navegable, pantalla a pantalla, en Markdown. Elige un papel y empieza a hacer clic como lo haría esa persona:

- **[Soy profesor](/docs/PROPUESTA_WIREFRAME/profesor/iniciarSesion.md)** -- entro, veo mis asignaturas, abro la guía de una de ellas, la edito, y la envío a revisión.
- **[Soy director de grado](/docs/PROPUESTA_WIREFRAME/directorGrado/iniciarSesion.md)** -- reviso las guías de mi grado, las apruebo o las rechazo, y gestiono asignaturas y resultados de aprendizaje.
- **[Soy administrador](/docs/PROPUESTA_WIREFRAME/admin/iniciarSesion.md)** -- doy de alta grados, asignaturas y profesorado, y genero el PDF de las guías ya aprobadas.

Cada pantalla es una imagen (el diseño) más una tabla de botones: pulsas uno y saltas a la siguiente pantalla, igual que en la aplicación real. Si un botón no tiene enlace es porque, en ese papel, no tienes permiso para pulsarlo -- es intencionado, no un enlace roto.

## 2. Cómo está pensado por dentro

Esto ya es el terreno de quien haya cursado ingeniería del software o le interese el oficio de diseñar un sistema antes de programarlo. Tres piezas, de la más conceptual a la más concreta:

- **[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md)** -- las entidades del sistema (`Guia`, `AsignaturaGrado`, `Profesor`...) y cómo se relacionan. Incluye el diagrama de estados de la `Guia`: Borrador, En revisión, Aprobada, Rechazada, y quién puede moverla de un estado a otro.
- **[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md)** -- quién usa el sistema (Profesor, DirectorGrado, Admin) y qué puede hacer cada uno, con el diagrama de estados de disponibilidad que marca qué acciones están vivas en cada momento.
- **[Detalle de casos de uso](/RUP/01-requisitos/03-detalle-casos-uso/README.md)** -- las 91 acciones del catálogo, una por una: qué pasos sigue, qué puede salir mal, y el wireframe de la pantalla correspondiente. Es el material del que sale el prototipo de la sección 1.

Todo el catálogo está enlazado entre sí -- el modelo de dominio explica el porqué de una regla, el diagrama de actores dice cuándo se puede invocar, el detalle cuenta el cómo paso a paso, y el mockup lo enseña en pantalla. Se puede entrar por cualquier puerta y llegar a las demás.

---

<sub>Varias fichas citan discussions/issues del repo de trabajo privado (`github.com/mmasias/pyCelda`) donde se debatió la decisión de modelado correspondiente -- son citas de procedencia, no enlaces navegables para quien no tenga acceso a ese repo; el texto que las acompaña ya explica la decisión sin necesidad de abrirlas. Este repo tampoco incluye las fases de Análisis/Diseño (aún sin empezar) ni el dashboard de seguimiento del proyecto.</sub>
