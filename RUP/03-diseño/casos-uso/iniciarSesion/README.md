<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > iniciarSesion() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/iniciarSesion/README.md)|[Análisis](/RUP/02-analisis/casos-uso/iniciarSesion/README.md)|**Diseño**|[Desarrollo](/RUP/04-desarrollo/casos-uso/iniciarSesion/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-24
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`iniciarSesion()`](/RUP/02-analisis/casos-uso/iniciarSesion/README.md): **dos** ramas `<<extend>>` mutuamente excluyentes según el rol identificado (`abrirInicio()` para `Profesor`/`DirectorGrado`, `abrirPanelAdministracion()` para `Admin` -- discussion [#274](https://github.com/mmasias/pyCelda/discussions/274) fusionó las dos primeras). Las ramas `Profesor`/`DirectorGrado` ya estaban en producción (discussion #62, `backend/app/routers/auth.py` + `backend/app/core/auth.py`) -- este documento las traduce retroactivamente. La rama `Admin` se resuelve aquí por primera vez a nivel de Diseño, con una decisión concreta que rompe la simetría del modelo de Análisis.

**Cambio de la discussion [#274](https://github.com/mmasias/pyCelda/discussions/274)**: la resolución de rol de `get_current_rol()` (en cada `GET /auth/me`, no en `callback()`) gana un guard -- el rol `director_grado` requiere dirigir `>= 1` `Grado` (`GradoRepository.contar_dirigidos_por(director.id) > 0`), no solo tener fila en `directores_grado`. Una fila huérfana de ex-director cae a `profesor` y, aun sin fila en `Profesor`, sigue resolviendo con éxito (rol `profesor`) -- **nunca 403 para una cuenta reconocida por el catálogo**. El payload de `/auth/me` gana `es_profesor` y `dirige_grados` (booleanos que [`abrirInicio()`](abrirInicio/README.md) consume para decidir qué secciones pinta); `es_tambien_profesor` se conserva para las pantallas de deep link. `Login.tsx` colapsa sus dos ramas de routing en una: `Profesor` y `DirectorGrado` navegan ambos a `/inicio`.

**Decisión central de este documento: `Admin` usa un endpoint de login físicamente separado, no una tercera rama del mismo `/auth/callback`.** Motivo (confirmado con Manuel): el historial de bugs de autorización del proyecto (ver `get_current_rol()` y la corrección de prioridad `DirectorGrado`/`Profesor` en issue #93) desaconseja mezclar la resolución de rol de `Admin` -- que hoy no tiene tabla propia -- con la de `Profesor`/`DirectorGrado` en el mismo camino de código.

**Corrección issue [#314](https://github.com/mmasias/pyCelda/issues/314)**: la última frase de arriba ("`Admin` no pasa por `get_current_rol()` en ningún momento") era imprecisa -- el *login* de `Admin` en efecto no pasa por `callback()`/`get_current_rol()` (eso sigue siendo así, endpoint separado como fija esta decisión), pero `/auth/me` sí es común a los tres roles (`RequireSession` lo llama en toda ruta autenticada del SPA, incluidas las de `Admin`), y antes de este fix `get_current_rol()` no reconocía el claim `rol=admin` del token en esa llamada -- un `Admin` puro (sin fila `Profesor`/`DirectorGrado`) quedaba con 403 en `/auth/me` y `RequireSession` lo expulsaba a `/`, aunque `require_admin()` sí aceptara su cookie en los endpoints reales de Admin. `get_current_rol()` gana una tercera rama, resuelta por el claim del token (sin consulta a BD, sin usar `AdminRepository`) antes de intentar `Profesor`/`DirectorGrado` -- no rompe la decisión de este documento (el login sigue siendo el endpoint separado de abajo), corrige el guard posterior que sí es compartido.

Consecuencia en el frontend: la pantalla de login deja de ser una sola. `Login.tsx` (ruta `/`) resuelve `Profesor`/`DirectorGrado` (y desde #274 navega a `/inicio` para ambos); una pantalla nueva, `AdminLogin.tsx` (ruta `/admin/login`), es el único punto de entrada al flujo de `Admin`. Esto no contradice el modelo de Análisis (`UsuarioNoLogueado` no puede saber su propio rol antes de autenticar): lo que el usuario elige de antemano no es su rol, es el *canal* (URL de login), exactamente igual que Requisitos ya trata "web/CLI/API" como independiente del caso de uso -- aquí el canal es "login general" vs. "login de administración", no una filtración de rol.

Este `secuencia.puml` contiene **dos diagramas**: el primero (`iniciarSesion-diseño`) es la implementación real de `Profesor`/`DirectorGrado`; el segundo (`iniciarSesion-admin-diseño`) es el diseño nuevo de la rama `Admin`, estructuralmente distinta (endpoint propio) -- mismo criterio de troceo que ya usa el proyecto para ficheros con más de un diagrama (`wireframes.puml` de Requisitos).

<div align=center>

|`Profesor`/`DirectorGrado` (real)|`Admin` (diseño nuevo)|
|:-:|:-:|
|![](/images/RUP/03-diseño/casos-uso/iniciarSesion/secuencia.svg)|![](/images/RUP/03-diseño/casos-uso/iniciarSesion/secuencia-admin.svg)|
|<sup>Código fuente: [secuencia.puml](secuencia.puml)</sup>|<sup>mismo fichero, segundo bloque `@startuml`</sup>|

</div>

## Participantes

### Rama Profesor/DirectorGrado (real, en producción)

- **Vista**: `Login.tsx` (React) -- botón "Iniciar sesión con Google", redirige a `GET /auth/login`; tras el retorno, cualquier sesión válida de `Profesor`/`DirectorGrado` navega a `/inicio` ([`abrirInicio()`](abrirInicio/README.md)).
- **API**: `routers/auth.py::login()` (redirect OAuth) / `::callback()` (intercambia el code, comprueba existencia, emite cookie con solo el email) / `::me()` -> `core/auth.py::get_current_rol()` (resuelve el rol y las señales `es_profesor`/`dirige_grados` en cada petición).
- **Modelo**: ninguno con lógica propia invocada -- la resolución es consulta de existencia + un `count`.
- **Repositorio**: `ProfesorRepository.obtener_por_email(email)`, `DirectorGradoRepository.obtener_por_email(email)`, `GradoRepository.contar_dirigidos_por(director_id)` (guard del rol `director_grado`, #274).

### Rama Admin (diseño nuevo)

- **Vista**: `AdminLogin.tsx` (React, no construida en esta rebanada) -- botón propio, redirige a `GET /auth/admin/login`.
- **API**: `routers/auth.py::login_admin()` (redirect OAuth, mismo cliente `Authlib`, `redirect_uri` propio) / `::callback_admin()` (intercambia el code, valida contra whitelist de configuración, emite cookie con claim `rol=admin` explícito).
- **Modelo/Repositorio**: ninguno -- deliberadamente no usa `AdminRepository` (introducida en Análisis de forma simétrica, ver más abajo).

## Decisiones de diseño

- **Endpoint separado para `Admin`, sin pasar por `get_current_rol()`**: `GET /auth/admin/login` + `GET /auth/admin/callback`, nuevas funciones en `routers/auth.py` (mismo módulo, no uno nuevo -- comparten el cliente `Authlib` ya configurado en `core/auth.py`, solo cambia el `redirect_uri` y la validación posterior). Nueva variable de entorno `OAUTH_ADMIN_REDIRECT_URI` (mismo patrón que `OAUTH_REDIRECT_URI` ya existente), registrada aparte en Google Cloud Console.
- **Whitelist de configuración, no `AdminRepository` contra una tabla**: nueva variable de entorno `ADMIN_EMAILS` (lista separada por comas). El `callback_admin()` valida `email in settings.admin_emails`, no una consulta a base de datos. Justificación: hoy no existe ninguna `crearAdmin()` en el catálogo de 91 casos de uso -- no hay mecanismo de alta para una tabla `admins`, así que una tabla real sería un dato sin forma de mantenerse. La `AdminRepository.obtenerPorEmail(email)` que introdujo el [Análisis de `iniciarSesion()`](/RUP/02-analisis/casos-uso/iniciarSesion/README.md) modela la simetría de Requisitos (tres ramas iguales) pero **no se usa en esta implementación** -- se deja documentado como el diseño al que se migraría el día que exista gestión real de `Admin` como entidad (tabla + CU de alta), sin coste de retrabajo de esquema (la whitelist y una tabla no son mutuamente excluyentes: se podría comprobar la tabla primero y la whitelist como fallback, o viceversa, cuando llegue ese momento -- decisión pospuesta a entonces).
- **Token con claim `rol=admin` explícito, a diferencia de `Profesor`/`DirectorGrado`**: la cookie de sesión de `Profesor`/`DirectorGrado` solo porta `email` -- el rol se re-resuelve en cada petición contra `DirectorGradoRepository`/`ProfesorRepository` (`get_current_rol()`). Para `Admin` no hay tabla que re-consultar, así que el rol se fija en el propio token en el momento del login (mismo mecanismo `joserfc`/`SESSION_SECRET_KEY` ya existente, payload con un campo `rol` adicional). La dependencia de autorización de los endpoints de `Admin` (`require_admin`, nueva en `core/auth.py`) decodifica el token y comprueba ese claim -- no reconsulta la whitelist en cada petición, evita el coste de releer `settings.admin_emails` en cada llamada y es coherente con que revocar el acceso de un Admin exige invalidar su sesión (igual que hoy no hay forma de revocar una sesión de `Profesor` a mitad de su vigencia salvo esperar a que expire).
- **`abrirUniversidades()`/`abrirFacultades()`/etc. (PR de Diseño en paralelo) quedan con una nota "autorización de Admin pendiente"**: deliberado, no un olvido. Esos 9 CU se diseñaron sin conocer todavía si `require_admin` existiría con ese nombre -- una vez fijado aquí, la dependencia a usar en cada uno de esos routers es `Depends(require_admin)`, mismo patrón que `Depends(get_current_director_grado_id)` ya usa `routers/grado.py`. No se ha retrofitado esa nota en los 9 ficheros para no ampliar el alcance de este documento -- queda como ajuste menor de Desarrollo, no de Diseño (la firma de la dependencia ya está fijada aquí, es integrarla).
- **Sin construir `AdminLogin.tsx` en esta rebanada**: se fija el endpoint (`/auth/admin/login`), no la pantalla -- mismo criterio que ya aplicó `configuracion-proyecto.md` a las 40 pantallas restantes del hilo `Guia`/`DirectorGrado` (Vista modelada como participante genérico, sin comprometer estructura de carpetas hasta que se construya).

## Referencias

- [`iniciarSesion()` en Análisis](/RUP/02-analisis/casos-uso/iniciarSesion/README.md) -- diagrama de colaboración origen, las dos ramas `<<extend>>` (Profesor/DirectorGrado -> `abrirInicio()`, Admin -> `abrirPanelAdministracion()`) y nota sobre `AdminRepository` sin implementación real.
- [`abrirInicio()` en Diseño](abrirInicio/README.md) -- destino del `<<extend>>` de `Profesor`/`DirectorGrado`; consume `es_profesor` / `dirige_grados` de `/auth/me`.
- `backend/app/routers/auth.py` / `backend/app/core/auth.py` -- implementación real de las ramas `Profesor`/`DirectorGrado`, base de la que se extienden las funciones nuevas de `Admin`.
- [`abrirPanelAdministracion()` en Diseño](/RUP/03-diseño/casos-uso/abrirPanelAdministracion/README.md) -- destino del `<<extend>>` de `Admin`, tras `callback_admin()`.
- Discussion [#62](https://github.com/mmasias/pyCelda/discussions/62) -- login real con Google, origen del mecanismo que se extiende aquí.
- Discussion [#113](https://github.com/mmasias/pyCelda/discussions/113) -- encargo de este Diseño, bloque "Admin bottom-up".
- Issue [#314](https://github.com/mmasias/pyCelda/issues/314) -- corrección: `get_current_rol()` gana la tercera rama `Admin` (token, sin BD); Admin puro bloqueado en producción.
