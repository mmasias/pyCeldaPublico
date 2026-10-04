<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > iniciarSesion() > Desarrollo

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/iniciarSesion/README.md)|[Análisis](/RUP/02-analisis/casos-uso/iniciarSesion/README.md)|[Diseño](/RUP/03-diseño/casos-uso/iniciarSesion/README.md)|**Desarrollo**|Pruebas|
> |-|-|-|-|-|-|-|

## Estado

✅ **Completado** -- ramas `Profesor`/`DirectorPrograma` en producción desde discussion #62, rama `Admin` desde el bloque "Admin bottom-up". Fusión de las ramas `Profesor`/`DirectorPrograma` en `abrirInicio()` + guard de rol: discussion [#274](https://github.com/mmasias/pyCelda/discussions/274).

## Cambio de la discussion #274 -- guard de rol y `/auth/me`

- **`core/auth.py::get_current_rol()`**: el rol `director_programa` requiere ahora `ProgramaRepository.contar_dirigidos_por(director.id) > 0`, no solo la fila en `directores_programa`. Una fila huérfana de ex-director (tras `quitarDirectorPrograma()`, que nunca la borra) cae a `profesor`; **si además no tiene fila en `Profesor`, sigue resolviendo con éxito (rol `profesor`) -- nunca 403 para una cuenta reconocida**. El payload gana `es_profesor` y `dirige_programas` (booleanos que `abrirInicio()` consume); `es_tambien_profesor` se conserva (== `rol == "director_programa" and es_profesor`).
- **`ProgramaRepository.contar_dirigidos_por(director_programa_id)`** -- nuevo, `SELECT count(*)` sobre `programas_directores_programa`.
- **`routers/programa.py::listar_programas`** y **`routers/asignatura_programa.py::listar_mis_asignaturas_programa`**: pasan a la variante `_opcional` de su dependencia de auth y devuelven `[]` (no `403`) para una cuenta sin esa capacidad -- `abrirInicio()` incluye siempre las dos secciones. Simétricos.
- **Frontend `Login.tsx`**: `Profesor` y `DirectorPrograma` navegan ambos a `/inicio`; se retira la bifurcación por `rol`.
- **Tests**: `tests/test_auth.py` -- `test_me_con_director_programa` invertido (ahora exige `>= 1` Programa), `test_me_director_sin_programas_cae_a_profesor`, `test_me_ex_director_sin_profesor_no_403_ni_bucle` (G3: `/auth/me` 200, sin bucle de `RequireSession`), `test_me_director_que_ademas_imparte_y_dirige_programa`, `test_programas_vacio_para_*` / `test_mis_asignaturas_vacio_para_director_puro` (endpoints -> `[]`). 604 en verde.

## Código (rama Admin, del bloque "Admin bottom-up")

## Código (rama Admin, nueva en esta rebanada)

- **Router**: [`routers/auth.py`](/backend/app/routers/auth.py) -- `login_admin()` (`GET /auth/admin/login`), `callback_admin()` (`GET /auth/admin/callback`)
- **Core**: [`core/auth.py`](/backend/app/core/auth.py) -- `create_admin_session_token(email)`, `require_admin(request)`
- **Config**: [`core/config.py`](/backend/app/core/config.py) -- `oauth_admin_redirect_uri`, `admin_emails` (whitelist `ADMIN_EMAILS`, lista separada por comas)
- **Tests**: [`tests/test_auth_admin.py`](/backend/tests/test_auth_admin.py)
- **Frontend**: [`pages/AdminLogin.tsx`](/frontend/src/pages/AdminLogin.tsx)

## Contrato de endpoint

### GET `/auth/admin/login`

Redirige a Google (mismo cliente `Authlib` que `/auth/login`), `redirect_uri` propio (`OAUTH_ADMIN_REDIRECT_URI`).

### GET `/auth/admin/callback`

Valida `hd` (dominio institucional) igual que `/auth/callback`. Comprueba el email contra `settings.admin_emails` -- **no** consulta `AdminRepository` ni ninguna tabla (introducida en Análisis para la simetría de Requisitos, sin uso real aquí, ver nota en el consolidado de Diseño). Si coincide, emite cookie de sesión vía `create_admin_session_token(email)` (claim `rol=admin` explícito) y redirige a `/panel-administracion`; si no, `403`.

### GET `/api/v1/version`

Sin autenticación (se consulta desde las pantallas de login, antes de tener sesión). Devuelve `{"esquema_version": int}`, leído de `PRAGMA user_version` de la base de datos. Código: [`routers/version.py`](/backend/app/routers/version.py), [`schemas/version.py`](/backend/app/schemas/version.py), `obtener_version_esquema()` en [`core/backups.py`](/backend/app/core/backups.py). Consumo en frontend: `obtenerVersion()` de [`api.ts`](/frontend/src/api.ts), en `Login.tsx` y `AdminLogin.tsx`, que lo muestran como sufijo "· esquema N" tras la versión de la app y lo omiten sin error si la llamada falla (issues #628, #630). El script de baseline [`scripts/fijar_version_esquema_inicial.py`](/backend/app/scripts/fijar_version_esquema_inicial.py) fija `user_version = 1` solo si vale 0.

## `require_admin` -- autorización real, verificada bloqueando

No reutiliza `get_current_rol()`. Decodifica la cookie, exige claim `rol == "admin"`. Aplicado a los 9 endpoints de `routers/universidad.py`/`routers/facultad.py`. (Hasta la corrección issue [#314](https://github.com/mmasias/pyCelda/issues/314) de abajo, `get_current_rol()` solo resolvía `Profesor`/`DirectorPrograma` -- ya no es el caso, pero `require_admin` sigue sin reutilizarlo por diseño, ver Diseño.)

**Verificado en vivo** contra el servidor real: una cookie de sesión de `Profesor` real (`manuel@masiasweb.com`, emitida por el mecanismo real de `create_session_token`) fue rechazada con `403` real al llamar a `/api/v1/universidades`; una cookie de `Admin` real (`manuel.masias@uneatlantico.es`, añadida a `ADMIN_EMAILS` en `.env` local) fue aceptada con `200`. No solo `pytest` -- petición HTTP real contra el proceso real y la BD real.

**Pendiente, no de esta rebanada**: el login real con Google en navegador (consentimiento OAuth de verdad) no se ha probado -- requiere la cuenta de Google real de Manuel, fuera del alcance de lo que esta sesión puede ejercitar. El mecanismo está probado con `_FakeGoogleClient` (mismo patrón que los tests ya existentes de `/auth/callback`), que sustituye la respuesta de Google sin red.

## Corrección issue #314 -- `get_current_rol()` gana la rama `Admin`

Bug en producción: un `Admin` puro (sin fila `Profesor`/`DirectorPrograma`, caso real de un Admin dado de alta poco antes) recibía `403` de `/auth/me` (`get_current_rol()` nunca miraba el claim `rol=admin` del token, caía directo a resolver `Profesor`/`DirectorPrograma`) y `RequireSession` lo expulsaba a `/`, pese a que `require_admin()` sí aceptaba su cookie en los endpoints reales de Admin.

- **`core/auth.py::get_current_rol()`**: guard temprano -- si `_decoded_admin_claims(request).get("rol") == "admin"`, devuelve el shape de Admin (`es_tambien_profesor`/`es_profesor`/`dirige_programas` en `False`) sin consultar `Profesor`/`DirectorPrograma`. Mismo criterio que `require_admin()`/`get_current_admin_email_opcional()`, sin `AdminRepository` ni tabla real.
- **Efecto secundario deliberado**: los 3 `Admin` previos que también tenían fila `Profesor`/`DirectorPrograma` pasan de resolver `profesor`/`director_programa` en silencio a resolver `admin` -- la clasificación correcta, no cambia nada observable (`PanelAdministracion.tsx` no lee `rol`).
- **Frontend**: `frontend/src/api.ts` -- `Rol` gana `"admin"`.
- **Tests**: `tests/test_auth.py` -- `test_me_con_admin_puro_sin_profesor_ni_director` (el caso real de Prometeus), `test_me_con_admin_que_tambien_es_profesor_resuelve_admin` (efecto secundario). 627 en verde.

## Referencias

- [`iniciarSesion()` en Diseño](/RUP/03-diseño/casos-uso/iniciarSesion/README.md) -- secuencia completa, decisión del endpoint separado, guard de rol de #274, corrección #314.
- `abrirInicio()` en Desarrollo -- pantalla `/inicio`, destino del `<<extend>>` de `Profesor`/`DirectorPrograma`.
- [`RUP/04-desarrollo/README.md`](/RUP/04-desarrollo/README.md#autenticación-real-google-oauth2oidc) -- implementación original de `Profesor`/`DirectorPrograma` (discussion #62), base de la que se extiende esta rama.
- Issue [#314](https://github.com/mmasias/pyCelda/issues/314) -- bug en producción y corrección de esta sección.
