<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# Desarrollo > Casos de uso (muestra de 5)

Elegidos para cubrir patrones distintos del proyecto, no los 5 más simples:

|Caso de uso|Por qué se eligió|
|-|-|
|[`crearGrado()`](crearGrado/README.md)|El patrón más básico: creación con validación de unicidad.|
|[`eliminarResultadoAprendizaje()`](eliminarResultadoAprendizaje/README.md)|Borrado protegido relacionalmente, con confirmación en dos pasos -- patrón muy común en sistemas reales.|
|[`iniciarSesion()`](iniciarSesion/README.md)|Autenticación real vía OAuth2 (Google), con varias ramas de resultado. Corrige de forma explícita en sus propios comentarios un error clásico de la literatura RUP: quién invoca el caso de uso antes de que exista el rol.|
|[`crearPonderacionEvaluacion()`](crearPonderacionEvaluacion/README.md)|Regla de negocio (validación de rango) resuelta en el propio modelo -- ilustra la decisión arquitectónica central del proyecto: Fat Model, sin capa Service.|
|[`enviarGuiaARevision()`](enviarGuiaARevision/README.md)|El más complejo de los cinco: varias condiciones encadenadas antes de aceptar la acción, evolucionado en varias iteraciones reales documentadas a lo largo del proyecto -- muestra cómo crece un caso de uso real con el tiempo, no solo el resultado final.|
