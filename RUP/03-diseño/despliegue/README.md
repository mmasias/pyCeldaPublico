<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# Diagrama de despliegue

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Vista física del sistema en producción: nodos reales, artefactos que corren en cada uno, y los protocolos de comunicación entre ellos. Complementa al [diagrama de clases de diseño](/RUP/03-diseño/diagrama-clases-diseño.puml) (vista OO) y al [modelo de datos](/RUP/03-diseño/modelo-datos/README.md) (vista relacional) -- este es el peldaño de la topología, no del código ni del esquema.

<div align=center>

|![](/images/RUP/03-diseño/despliegue/despliegue.svg)|
|-|
|<div align=right><sup>Código fuente: [despliegue.puml](despliegue.puml)</sup></div>|

</div>

## Lectura del diagrama

**Un único host, sin orquestador**: `Prometeus`, un Fedora doméstico, corre los dos contenedores con `docker compose`. No hay balanceo ni réplicas -- decisión consciente mientras no haya uso real concurrente que lo justifique.

**El frontend no tiene contenedor propio**: `Dockerfile.caddy` es un build multi-stage que compila `frontend/` (`npm run build`) y copia `dist/` dentro de la propia imagen de Caddy, que lo sirve como estático (`file_server` + `try_files` para el fallback de SPA). Es la razón por la que el diagrama dibuja `caddy` con dos artefactos (reverse proxy y SPA), no dos nodos separados.

**Caddy reparte por ruta, no todo va al backend**: `/api/*` y `/auth/*` van por `reverse_proxy` al contenedor `backend:8000` (red interna de Docker, sin puerto expuesto al host); todo lo demás se sirve directo desde `/srv`. Un `curl` a `/` nunca ejercita el backend ni la base de datos -- por eso el health-check real es `GET /api/health` (`SELECT 1` contra SQLAlchemy), no la raíz.

**Un solo volumen de datos, sin réplica, con backup diario automatizado**: `pycelda-db` contiene el único fichero SQLite del sistema. Dos mecanismos de copia, ninguno dentro de Docker: `pycelda-db-backup-puntual.sh` (invocado a mano antes de cada migración de esquema, backup "puntual") y un timer de `systemd --user` (`pycelda-backup.timer`, issue [#185](https://github.com/mmasias/pyCelda/issues/185)) que dispara uno "diario" cada 24h -- infraestructura del host, fuera del repo, verificada activa por `Claude-pyCelda-Prometeus` (`systemctl --user list-timers`). Ambas familias quedan registradas en `backups_manifest.jsonl` (issue [#308](https://github.com/mmasias/pyCelda/issues/308)), consultable desde `consultarCopiasSeguridad()`.

**TLS gestionado por Caddy solo**: `caddy-data` guarda los certificados de Let's Encrypt, renovados automáticamente por el propio binario de Caddy -- ningún componente de la aplicación toca TLS.

## Fuera de este diagrama

Detalle operativo completo (reglas de `Deploy:` en el commit, ritual de `Claude-pyCelda-Prometeus`, bugs de infraestructura ya corregidos) vive en `/DEPLOY.md`, no aquí -- ese documento cambia con el proceso, este diagrama cambia con la topología. Configuración fuera de git (DNS/DDNS, secretos de `.env`, firewall del host) tampoco se representa: es responsabilidad operativa directa de Manuel, sin rastro en el repo.
