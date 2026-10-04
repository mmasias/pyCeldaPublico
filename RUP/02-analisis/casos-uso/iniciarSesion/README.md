<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > iniciarSesion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/iniciarSesion/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/iniciarSesion/README.md)|[Desarrollo](/RUP/04-desarrollo/casos-uso/iniciarSesion/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`iniciarSesion()`](/RUP/01-requisitos/03-detalle-casos-uso/iniciarSesion/README.md): un único punto de extensión ("tras validación exitosa"), **dos** ramas mutuamente excluyentes según el rol identificado (`<<extend>>` de [`abrirInicio()`](../abrirInicio/README.md) para `Profesor`/`DirectorPrograma` y de [`abrirPanelAdministracion()`](../abrirPanelAdministracion/README.md) para `Admin`, ninguna con contenido propio aquí), más el fallo (self-loop sin cambio de estado). Antes eran tres (una por rol); la fusión de las ramas de `Profesor` y `DirectorPrograma` en `abrirInicio()` se cierra en la [discussion #274](https://github.com/mmasias/pyCelda/discussions/274).

**Modelado retroactivo, no de un CU nuevo**: las ramas de `Profesor`/`DirectorPrograma` ya están en producción (`backend/app/routers/auth.py`, `backend/app/core/auth.py`, `frontend/src/pages/Login.tsx`) -- se construyeron directo a código (discussion [#62](https://github.com/mmasias/pyCelda/discussions/62)) sin pasar nunca por `colaboracion.puml`. Este documento las traduce a clases de análisis para dejar el patrón consistente con el resto del catálogo, no para volver a decidir nada ya cerrado.

**El mecanismo real no es "usuario y contraseña"**: es autenticación delegada a Google (OAuth2/OIDC), restringida al dominio institucional de Workspace (parámetro `hd`), sin auto-registro -- el email de la cuenta de Google tiene que coincidir con un `Profesor`, `DirectorPrograma` o `Admin` ya existente en el catálogo (creados por `Admin` vía `crearProfesor()`/`definirDirectorPrograma()`, fuera de esta rebanada). Un email puede resolver a `DirectorPrograma` y `Profesor` a la vez (`DirectorPrograma -u-|> Profesor`, roles no exclusivos) -- la resolución prioriza `DirectorPrograma` **si dirige `>= 1` `Programa`** (discussion [#274](https://github.com/mmasias/pyCelda/discussions/274); una fila sin programas a su cargo cae a `profesor`), y `abrirInicio()` compone ambos listados cuando la cuenta tiene las dos capacidades, sin que la prioridad importe ya para el enrutado. El `<<choice>>` de Requisitos ("validación exitosa" / "credenciales inválidas") se traduce aquí a esa resolución contra el catálogo, no a comparar una contraseña.

**Rama de `Admin`, sin implementación real todavía**: el modelo de Requisitos es simétrico entre los tres roles, y este documento lo traduce con la misma simetría (`AdminRepository.obtenerPorEmail(email)` junto a `ProfesorRepository`/`DirectorProgramaRepository`). En el código real de hoy, `callback()` (`backend/app/routers/auth.py`) solo consulta `ProfesorRepository`/`DirectorProgramaRepository` -- ni el modelo `Admin` ni `AdminRepository` existen todavía en `backend/app/models/`/`backend/app/repositories/` (confirmado, no hay `admin.py` en ninguno de los dos directorios). Coherente con la nota ya cerrada en el modelo de dominio (`RUP/00-modelo-del-dominio/README.md`, línea 29): "el login de `Admin` se prueba cuando exista su mini-rebanada propia". Ya se discutió con Manuel que, en Diseño, la rama de `Admin` tendrá un endpoint separado (`/auth/admin/login`, whitelist propia, JWT sin pasar por `get_current_rol()`) por el historial de bugs de autorización del proyecto -- decisión de Diseño de esta misma CU. La rama de `Admin` (`<<extend>>` de `abrirPanelAdministracion()`) es simétrica y no cambia con la discussion #274 -- lo que se fusiona es solo `Profesor`/`DirectorPrograma` en `abrirInicio()`.

**Corrección issue [#314](https://github.com/mmasias/pyCelda/issues/314) -- `get_current_rol()` sí resuelve `Admin`, como tercera rama vía token, no vía `AdminRepository`**: el párrafo anterior queda desactualizado en un punto concreto -- `get_current_rol()` (`GET /auth/me`, llamado por `RequireSession` en TODAS las rutas autenticadas del SPA, incluidas las de `Admin`) antes nunca miraba el claim `rol=admin` del token y caía directo a resolver `Profesor`/`DirectorPrograma`; un `Admin` puro (sin fila en ninguna de las dos tablas) recibía el 403 de "Cuenta sin rol asociado" y `RequireSession` lo expulsaba a `/`, pese a que `require_admin()` (el guard real de los endpoints de escritura de `Admin`) sí lo aceptaba -- caso real de un Admin sin fila en Profesor/DirectorPrograma. El fix añade un guard temprano: si el claim `rol=admin` está presente (fijado por `create_admin_session_token()` en el login de Admin, mismo mecanismo que ya usa `require_admin()`), `SesionController` corta ahí y devuelve el rol `admin` sin consultar `Profesor`/`DirectorPrograma` -- sigue sin haber `AdminRepository` real contra una tabla (ese repositorio de Análisis sigue sin implementación, ver Diseño), la resolución es puramente del token. Efecto secundario deliberado: los `Admin` que además tienen fila `Profesor`/`DirectorPrograma` (los 3 admins previos al nuevo Admin) pasan de resolver `profesor`/`director_programa` en silencio a resolver `admin`, la clasificación correcta.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/iniciarSesion/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `IniciarSesionView`

**Responsabilidades:**
- ofrece el botón de inicio de sesión con Google -- no hay formulario de credenciales propio: la validación de identidad la resuelve el proveedor externo, no el sistema.
- en la rama roja, presenta el mensaje de credenciales inválidas / cuenta no autorizada.

**Colaboraciones:**
- **Entrada:** `:SESION_CERRADA` -- el `UsuarioNoLogueado` solicita iniciar sesión.
- **Control:** `SesionController`.
- **Salida:** `:Collaboration AbrirInicio` (si `rol in {Profesor, DirectorPrograma}`) / `:Collaboration AbrirPanelAdministracion` (si `rol == Admin`) o `:SESION_CERRADA` (fallo).

## Clases de controlador

### `SesionController`

**Responsabilidades:**
- inicia el flujo de autenticación delegada (`autenticarConGoogle()`) -- redirige al proveedor externo, sin validar nada localmente.
- tras el retorno del proveedor (callback), valida el dominio institucional y resuelve el rol de la cuenta autenticada contra el catálogo interno (`resolverRol(email)`): consulta `DirectorPrograma`/`Profesor`/`Admin` en ese orden de prioridad -- sin ninguna coincidencia, rechaza (sin auto-registro).
- el rol `director_programa` requiere que el email dirija `>= 1` `Programa` (fila en `DirectorPrograma` **y** pertenencia a la colección `directores` de algún `Programa`), no solo la fila -- discussion [#274](https://github.com/mmasias/pyCelda/discussions/274). Una fila huérfana de ex-director cae a `profesor`; si además no imparte, sigue resolviendo con éxito (rol `profesor`), **nunca rechaza** -- una cuenta autenticada y reconocida por el catálogo no se expulsa, la capacidad ausente la absorbe `abrirInicio()` como sección vacía. El `<<choice>>` no ramifica ese caso degenerado.
- señaliza además, para `abrirInicio()`, las dos capacidades independientes de la cuenta: `esProfesor` (fila en `Profesor`) y `dirigeProgramas` (dirige `>= 1` `Programa`) -- `es_tambien_profesor` de la implementación real es una de ellas.
- emite el token de sesión tras resolver el rol con éxito (`crearSesion(email)`).

**Colaboraciones:**
- **Entrada:** `IniciarSesionView`.
- **Salida:** `DirectorProgramaRepository`, `ProfesorRepository`, `AdminRepository`.

## Clases de modelo

### `Profesor`

Ya existente en el consolidado (`AsignaturaPrograma -- Profesor`, `AsignaturaProgramaController.listarProfesoradoAsignado(asignaturaProgramaId)`) -- sin cambios aquí.

### `ProfesorRepository`

**Responsabilidades:**
- recupera el `Profesor` por email (`obtenerPorEmail(email)`) -- coincidencia exacta contra el catálogo, sin auto-registro.

**Colaboraciones:**
- **Entrada:** `SesionController`.
- **Salida:** gestiona `Profesor`.

### `DirectorPrograma`

**Responsabilidades:**
- ninguna propia más allá de identificar el rol -- `DirectorPrograma -u-|> Profesor` en el modelo de dominio (hereda `email`), primera aparición como clase de Análisis en este catálogo.

**Colaboraciones:**
- **Entrada:** recuperado por `DirectorProgramaRepository`.

### `DirectorProgramaRepository`

**Responsabilidades:**
- recupera el `DirectorPrograma` por email (`obtenerPorEmail(email)`) -- se consulta antes que `ProfesorRepository`, pero solo cuenta como rol `director_programa` si además dirige `>= 1` `Programa` (discussion [#274](https://github.com/mmasias/pyCelda/discussions/274)); si no, la cuenta con doble identidad resuelve como `profesor`.

**Colaboraciones:**
- **Entrada:** `SesionController`.
- **Salida:** gestiona `DirectorPrograma`.

### `Admin`

**Responsabilidades:**
- ninguna propia más allá de identificar el rol -- primera aparición como clase de Análisis en este catálogo, simétrica a `Profesor`/`DirectorPrograma` en el modelo de Requisitos.

**Colaboraciones:**
- **Entrada:** recuperado por `AdminRepository`.

### `AdminRepository`

**Responsabilidades:**
- recupera el `Admin` por email (`obtenerPorEmail(email)`) -- simétrico a `ProfesorRepository`/`DirectorProgramaRepository` en el modelo de Requisitos. Sin implementación real todavía (ver Propósito).

**Colaboraciones:**
- **Entrada:** `SesionController`.
- **Salida:** gestiona `Admin`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/iniciarSesion/especificacion.puml) -- fuente de verdad de las dos ramas `<<extend>>` y el fallo. Esta carpeta no tiene `wireframes.puml` propio (ninguna rama tiene contenido propio aquí, ver ficha de Requisitos).
- [`abrirInicio()`](../abrirInicio/README.md) -- destino del `<<extend>>` para `Profesor`/`DirectorPrograma`; primitiva que `<<include>>` los dos listados.
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) / [DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) / [Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SESION_CERRADA --> X : iniciarSesion()`: `INICIO_ABIERTO` para Profesor y DirectorPrograma (mismo destino desde #274), `SISTEMA_DISPONIBLE` para Admin.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `DirectorPrograma -u-|> Profesor`, `Admin.email` (nota de la línea 29 del README de esa fase sobre el gap de implementación).
- `backend/app/routers/auth.py` / `backend/app/core/auth.py` -- implementación real (Profesor/DirectorPrograma) de la que se retroalimenta este documento.
- [`abrirAsignaturasPrograma()`](../abrirAsignaturasPrograma/README.md) -- variante `Profesor` (wireframe "MIS ASIGNATURAS"), incluida por `abrirInicio()` como sección "Mis guías".
- [`abrirProgramas()`](../abrirProgramas/README.md) -- variante `DirectorPrograma`, incluida por `abrirInicio()` como sección "Mis programas".
- [`abrirPanelAdministracion()`](../abrirPanelAdministracion/README.md) -- extendido para `Admin`.
- Discussion [#62](https://github.com/mmasias/pyCelda/discussions/62) -- login real con Google, origen de la implementación retroactivamente modelada aquí.
- Discussion [#113](https://github.com/mmasias/pyCelda/discussions/113) -- encargo de este Análisis, bloque "Admin bottom-up".
- Issue [#314](https://github.com/mmasias/pyCelda/issues/314) -- corrección: `get_current_rol()` gana la tercera rama `Admin` (token, sin BD); Admin puro bloqueado en producción.
