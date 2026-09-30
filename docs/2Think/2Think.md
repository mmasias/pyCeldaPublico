# pyCelda

## ¿Por qué?

Cada curso académico, cada asignatura de cada programa necesita una guía docente: temario, sistema de evaluación, bibliografía, planificación de sesiones, resultados de aprendizaje, metodologías. Documentos sujetos a baremos de ANECA, que deben ser coherentes entre sí dentro del mismo programa, y que hasta ahora vivían dispersos en Word -- un fichero por asignatura, por profesor, por curso académico, sin trazabilidad de quién cambió qué ni cuándo, sin ninguna garantía estructural de que la suma de ponderaciones diera 100%, ni de que el mismo código de metodología docente significara lo mismo en dos programas distintos.

Este último punto no es hipotético: durante el desarrollo del proyecto se encontró que las metodologías docentes presentaban casos de divergencia en codificación según el programa en el que se usara: no un caso aislado, sino la firma de un sistema sin control real de catálogo.

## ¿Qué?

pyCelda formaliza ese proceso en un modelo de datos, construido disciplina a disciplina siguiendo RUP: 109 casos de uso especificados de extremo a extremo (Requisitos, Análisis, Diseño, Desarrollo, Pruebas, Despliegue), 106 implementados con un test real detrás de cada uno.

| Qué | Cantidad real |
| --- | --- |
| Programas | 16 |
| Materias | 252 |
| Asignaturas dentro de un programa | 853 |
| Asignaturas de catálogo institucional | 402 |
| Guías docentes completas | 775 |
| Metodologías docentes institucionales | 10 |
| Resultados de aprendizaje repartidos | 5.048 |

Ese corpus reconciliado (16 programas oficiales) parte de un corpus histórico mayor: 834 guías docentes reales en Word, extraídas y parseadas en 2 días (`extractor.py`, ver `docs/scripts/README.md`) -- 9 facultades, 36 grados detectados en la nomenclatura real, 375 asignaturas de catálogo, 803 asignaturas-en-grado, 216 profesores. La reconciliación posterior contra las memorias verificadas de ANECA es la que redujo esos 36 grados detectados a los 16 programas oficiales de la tabla anterior.

## ¿Para qué?

Importar el corpus completo -- los 16 programas reales, con todas sus materias, asignaturas, resultados de aprendizaje repartidos en cascada, ponderaciones de evaluación y bibliografía de cada guía, validado contra las reglas estructurales del sistema -- tarda 23,5 segundos, sin errores. Medido hoy mismo, contra una base SQLite en memoria, con el script real de importación (`cargar_programa()`).

No hay una cifra medida de lo que costaba el proceso manual anterior -- no se llevó registro. Como estimación, no medición, ajustable: a una hora por guía entre redacción, formateo y revisión cruzada contra los baremos ANECA, las 775 guías del corpus equivaldrían a unas 96 jornadas de 8 horas. Es una suposición razonable, no un dato verificado.

Ese import de segundos no es el único valor. A quien lo usa cada día le resuelve tres cosas distintas: al profesor, redactar y mantener la guía sin retipear temario ni bibliografía cada curso -- puede importarlos de una asignatura hermana ya aprobada, y sabe en todo momento en qué estado exacto está su guía; a la auditoría de calidad (ANECA), consultar un catálogo con las ponderaciones ya verificadas contra rango y un historial completo de quién aprobó qué, en vez de pedir y revisar guía a guía; y a la ordenación académica, un catálogo único de facultades, programas y profesorado, con garantía de que un código de asignatura o de metodología significa lo mismo en cualquier programa. Resolver esto para los tres a la vez es la base de la que parten las aplicaciones satélite descritas en "¿Y ahora qué?" -- ninguna sería viable sin este catálogo ya validado.

## ¿Cómo?

No es solo velocidad. Cada guía que entra en pyCelda pasa, sin que nadie tenga que acordarse de comprobarlo a mano:

| Garantía | Qué impide |
| --- | --- |
| Rango ANECA | Una ponderación fuera del mínimo/máximo verificado de su sistema de evaluación, o una guía cuya suma de ponderaciones no sea exactamente 100% |
| Cascada de catálogos (Programa -> Materia -> Asignatura) | Que una metodología docente, resultado de aprendizaje o actividad formativa llegue a una asignatura sin haber sido habilitada antes por su programa y su materia |
| Ciclo de vida gobernado (4 estados, 11 transiciones) | Que alguien sin autoridad apruebe, rechace o edite una guía fuera de su rol -- el profesor redacta, el director decide, el admin nunca decide contenido |
| Historial íntegro | Una edición sin autor, campo, valor anterior y valor nuevo registrados |
| Copia de seguridad diaria automatizada | Pérdida de datos entre backups manuales |
| Auditoría externa independiente (dos modelos de IA sin coordinarse) | Redundancias, contradicciones o huecos de trazabilidad sin detectar -- cero encontrados sobre el catálogo completo de casos de uso |

Auditoría del 2026-08-08, sobre el catálogo de 91 casos de uso vigente entonces -- no repetida sobre los 109 actuales.

## ¿Y ahora qué?

A partir de aquí se puede -sin sobrecargar o pervertir pyCelda- desarrollar un conjunto de soluciones satélites: ninguna de las siguientes existe todavía. Se listan porque, si se construyen, no requerirían volver a modelar programas, materias, profesores o guías -- reutilizarían y extenderían el catálogo ya validado y las soluciones a las que se tendria acceso.

| Aplicación satélite | Qué añadiría | Para |
| --- | --- | --- |
| pyMERITOS | Monitor de información docente, sobre PerfilProfesorCurso (ORCID, CVN, acreditación SIIU, sexenios) ya modelado | RRHH |
| pyINDICADORES | Gestor de indicadores institucionales | Calidad, Ordenación académica |
| pyENCUESTADOR | Gestor de encuestas docentes | Alumnos, Directores de grado, Calidad |
| pyPUBLICA | Portal público de consulta de las guías aprobadas del curso activo | ANECA, alumnos, externos |
| pyBIBLIOTECA | Normalizador de referencias bibliográficas | Profesores |
| pyCOORDINA | Detector de sobrecarga de evaluación a partir de la planificación docente real | Directores de grado |
| pySESION | Control de eventos, presencia y asistencia | Profesores |
| pyFEDATARIO | Notarización y personalización de guías por alumno | Secretaría académica |
| pySIGHOR | Gestor de horarios | Ordenación académica |
| pyACTIVITAT | Gestor de actividad docente del profesorado | Secretaría general |
