<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# Desarrollo

Fase que baja el [`secuencia.puml`](/RUP/03-diseño/README.md) de Diseño a código real -- **enlaza a los ficheros del repo, no los duplica**. Cada `README.md` de caso de uso documenta el contrato de endpoint (request/response de ejemplo) y un campo Estado.

**En pyCelda real, esta fase cubre prácticamente todo el catálogo** (más de 90 casos de uso con código real). Este espejo público solo trae **5 casos de uso elegidos como muestra representativa** -- ver [casos de uso](casos-uso/README.md) -- para que se pueda leer el recorrido completo Requisitos -> Análisis -> Diseño -> Desarrollo sobre ejemplos concretos, sin exponer el código de la aplicación entera.

## Código

`backend/app/` -- estructura y stack fijados en [`RUP/03-diseño/configuracion-proyecto.md`](/RUP/03-diseño/configuracion-proyecto.md):

- [`models/`](/backend/app/models) -- SQLAlchemy, Fat Model (`Guia.confirmar_guardado()`, `SistemaEvaluacion.validar_maximo()`, ...), sin capa Service.
- [`schemas/`](/backend/app/schemas) -- Pydantic, request/response de cada endpoint.
- [`repositories/`](/backend/app/repositories) -- CRUD puro.
- [`routers/`](/backend/app/routers) -- funciones sueltas decoradas, sin capa Service.
- [`tests/`](/backend/tests) -- un fichero por caso de uso, casos positivos y negativos.

`frontend/src/` -- React + TypeScript, sin framework de estado global (`useState`/`fetch` directo).
