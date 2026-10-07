<div align=right>

<sub>[Manual de Profesor](README.md)</sub>

</div>

# Entrar y ver las asignaturas

## Cómo entrar

1. Abrir pyCelda en el navegador. Aparece la pantalla **Módulo académico** con el botón **🔑 Iniciar sesión** (la autenticación es con Google) y, en la misma línea, los enlaces a los manuales. Al pie, en pequeño, se ve la versión de la aplicación y la de esquema (p. ej. `Versión v0.11.8 · esquema 2`).
2. Pulsar el botón e iniciar sesión con la cuenta de correo de la universidad dada de alta por Admin. Con otra cuenta, el acceso no se completa.
3. Tras iniciar sesión, la pantalla de destino es **Inicio**. Todas las pantallas del modo académico llevan una **barra naranja** fija en el borde superior de la ventana: es la señal de que se está en el modo del profesorado y los directores (el modo Admin tiene una barra azul).

Si la cuenta no está dada de alta como profesor, corresponde contactar con Admin: pyCelda no permite crear una cuenta propia desde la pantalla de entrada.

## Primero, confirmar el perfil del curso

Al empezar cada curso académico, el perfil académico hay que confirmarlo una vez. Mientras no esté confirmado, **Inicio** no muestra las guías, sino el aviso "Debes confirmar tu perfil académico de este curso antes de continuar", que remite al botón **🪪 Mi perfil** de arriba a la derecha. El capítulo [Mi perfil](miPerfil.md) explica cómo hacerlo; al guardar el perfil, Inicio ya muestra las guías.

## Qué muestra Inicio

En **Inicio** aparece la sección **Mis guías**. Debajo del título, una línea resume cuántas guías hay en cada estado (por ejemplo, "6 guías: 1 rechazada, 2 en borrador, 3 aprobadas"), empezando por lo que más pide atención. Debajo, una tabla con una fila por cada asignatura impartida en el curso.

Columnas de la tabla:

- **Asignatura**.
- **Código**: el código de la asignatura.
- **Programa** (si la misma asignatura se imparte en varios programas, aparece una fila por programa).
- **Curso**: el curso en números romanos y el semestre por defecto combinados (p. ej. **II-s1**). La tabla se ordena por semestre, luego curso y nombre.
- **Carácter**: Básica, Obligatoria, Optativa, etc.
- **Estado**: el estado actual de la guía docente de esa asignatura -- Borrador, En revisión, Aprobada o Rechazada --, escrito sobre un fondo de color para distinguirlos de un vistazo. Si la guía se ha rechazado o se ha revocado su aprobación, el comentario del director aparece debajo, en cursiva. El significado de cada estado se explica en el capítulo [Redactar la guía](redactarLaGuia.md).
- **Guía**: el botón **📂 Abrir**, que lleva a la guía correspondiente. Si el botón no aparece en una fila, es que esa asignatura todavía no tiene una guía creada -- corresponde avisar a Admin.

Si la cuenta no imparte ninguna asignatura este curso, en lugar de la tabla aparece el mensaje "No tienes asignaturas asignadas".

Si la cuenta también dirige algún programa y hay guías esperando su revisión, Inicio lo indica en una línea encima de **Mis guías** (ver el [manual de Director de Programa](../directorPrograma/README.md)).

## Moverse por pyCelda

Arriba a la derecha de cada pantalla están siempre los mismos accesos, en este orden:

- **🏠 Inicio**: vuelve a esta pantalla desde cualquier sitio.
- **🎓 Mis programas**: solo si la cuenta dirige algún programa.
- **🪪 Mi perfil**: el perfil académico del curso.
- Debajo, en algunos formularios, su salida propia (por ejemplo, **Volver a las Ponderaciones**). Las pantallas de evaluación, bibliografía y planificación no tienen botón de volver: su título es una miga (**asignatura › Evaluación**) y pulsar el nombre de la asignatura vuelve a la guía.
- Al final, algo separado para no pulsarlo por error, **🚪 Cerrar sesión**.

No aparece el acceso de la pantalla en la que ya se está. En los formularios de crear o editar no hay accesos: se sale con **Guardar** o con su salida propia (**Cancelar**, o **Volver a las Ponderaciones** y **Volver a las Referencias bibliográficas** en los de evaluación y bibliografía).

---

<div align=center>

|  | [Índice](README.md) | [Mi perfil](miPerfil.md) |
|---|:-:|---|

</div>
