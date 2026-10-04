<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirMetodologiasDocentesPrograma() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiasDocentesPrograma/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirMetodologiasDocentesPrograma/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-19
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`abrirMetodologiasDocentesPrograma()`](/RUP/02-analisis/casos-uso/abrirMetodologiasDocentesPrograma/README.md): un solo paso, sin `<<choice>>`, de solo lectura. **Sin cambios de backend**: reutiliza el endpoint de listado ya existente (actor-agnóstico) que consumía la sección embebida de `abrirPrograma()`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirMetodologiasDocentesPrograma/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `MetodologiasDocentesPrograma.tsx` (React, ruta `/programas/:id/metodologias-docentes`) -- pide `obtenerPrograma()` y `GET /api/v1/programas/{programa_id}/metodologias-docentes` en paralelo; presenta `codigo`, `descripcion` por fila.
- **API**: `routers/programa.py::listar_metodologias_docentes_del_programa(programa_id)` -- ya existente.
- **Modelo**: ninguno con lógica propia invocada.

## Decisiones de diseño

- **Pantalla propia, no sección embebida**: sigue el patrón de `ResultadosAprendizaje.tsx` (página colgada de `NavPrograma`, botón "🧩 Metodologías" entre "Resultados de aprendizaje" y "Asignaturas"). `Admin` tiene su propia pantalla (`MetodologiasDocentesProgramaAdmin.tsx`, patrón de `MateriasAdmin.tsx`: un único "Volver", sin menú persistente; botón "🧩 Ver Metodologías" en `ProgramaAdmin.tsx`) desde el issue #640.
- **Retorno de asociar/desasociar**: `AsociarMetodologiaDocentePrograma` y `DesasociarMetodologiaDocentePrograma` vuelven a esta pantalla, no a `/programas/:id`.

## Referencias

- [`abrirMetodologiasDocentesPrograma()` en Análisis](/RUP/02-analisis/casos-uso/abrirMetodologiasDocentesPrograma/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiasDocentesPrograma/README.md).
- [`abrirResultadosAprendizaje()` en Diseño](/RUP/03-diseño/casos-uso/abrirResultadosAprendizaje/README.md) -- precedente de pantalla propia.
