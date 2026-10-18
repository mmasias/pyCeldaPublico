import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { API_BASE, obtenerSesion, obtenerVersion } from "../api";
import { URL_MANUAL_ADMIN } from "../manualUsuario";
import { useFondoModoAdmin } from "../useFondoModoAdmin";

export default function AdminLogin() {
  useFondoModoAdmin();
  const navigate = useNavigate();
  const [esquemaVersion, setEsquemaVersion] = useState<number | null>(null);

  useEffect(() => {
    // Dato informativo, no crítico: si falla, se omite el sufijo sin error visible.
    obtenerVersion()
      .then((r) => setEsquemaVersion(r.esquema_version))
      .catch(() => {});
  }, []);

  useEffect(() => {
    // Con el acceso cruzado entre logins, esta pantalla ya no es alcanzable
    // solo desde "/": un Admin con la sesión abierta que abriera el marcador
    // de /admin/login (o volviera con Atrás desde el panel) vería el login y,
    // con el cuadrado naranja, pasaría a "/" -- y Login le redirigiría a
    // /inicio, una pantalla que no es la suya (la cookie es compartida y el
    // token rol=admin anula el académico, #314). Misma comprobación que
    // Login: si ya hay sesión de Admin, directo al panel; sesión académica
    // o sin sesión -> se queda aquí para iniciar sesión de Admin.
    obtenerSesion()
      .then((sesion) => {
        if (sesion.rol === "admin") {
          navigate("/panel-administracion", { replace: true });
        }
      })
      .catch(() => {
        // sin sesión válida -- se queda en AdminLogin para iniciar sesión
      });
  }, [navigate]);

  function iniciarSesionConGoogle() {
    window.location.href = `${API_BASE}/auth/admin/login`;
  }

  return (
    <main>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "0.25rem",
          padding: "1rem 1.5rem",
          backgroundColor: "#f3f4f6",
          borderRadius: "8px 8px 0 0",
          // Borde fino del color de la barra superior del modo Admin (azul); el
          // inferior, negro y más grueso, separa del resto de la pantalla.
          borderTop: "1px solid #337ab7",
          borderLeft: "1px solid #337ab7",
          borderRight: "1px solid #337ab7",
          borderBottom: "2px solid #000",
          marginBottom: "1rem",
          position: "relative",
        }}
      >
        {/* Acceso cruzado entre las dos pantallas de login: cuadrado naranja,
            el color de la barra del modo ACADÉMICO (index.css,
            html.modo-academico::before) -- el color indica adónde se va. Sin
            texto y pequeño para no competir con el login; title/aria-label
            lo hacen accesible a teclado y lectores. Solo entre logins: no
            hay paso directo de una sesión abierta a la otra (cookie y token
            compartidos, #314). */}
        <Link
          to="/"
          title="Módulo docente"
          aria-label="Módulo docente"
          style={{
            position: "absolute",
            top: "0.5rem",
            right: "0.5rem",
            width: "1.25rem",
            height: "1.25rem",
            backgroundColor: "#f6871f",
            borderRadius: "4px",
            display: "block",
          }}
        />
        <div style={{ display: "flex", alignItems: "flex-end", gap: "1rem" }}>
          <img
            src="/logo-hexagono.png"
            alt="CELDA"
            style={{ width: "112px", height: "112px", border: "1px solid #d0d5dd" }}
          />
          <h1 style={{ fontSize: "2.5rem", margin: 0, lineHeight: 1 }}>CELDA</h1>
        </div>
        <p style={{ margin: 0 }}>
          <sub><i>Catálogo ELectrónico de Documentación Académica</i></sub>
        </p>
      </div>
      <p style={{ margin: 0 }}>
        <b>Módulo de administración</b>
      </p>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", margin: "1rem 0" }}>
        <button onClick={iniciarSesionConGoogle}>
          🔑 Iniciar sesión
        </button>
        <span>
          <sub style={{ fontSize: "0.75em" }}>
            <a href={URL_MANUAL_ADMIN} target="_blank" rel="noreferrer">
              Manual del administrador
            </a>
          </sub>
        </span>
      </div>
      <hr />
      <p style={{ textAlign: "right", margin: 0 }}>
        <sub style={{ fontSize: "0.7em", fontStyle: "italic", color: "#555" }}>
          Versión v{__APP_VERSION__}{esquemaVersion !== null ? ` · esquema ${esquemaVersion}` : ""}
        </sub>
      </p>
    </main>
  );
}
