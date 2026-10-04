import { useEffect, useState } from "react";
import { API_BASE, obtenerVersion } from "../api";
import { URL_MANUAL_ADMIN } from "../manualUsuario";
import { useFondoModoAdmin } from "../useFondoModoAdmin";

export default function AdminLogin() {
  useFondoModoAdmin();
  const [esquemaVersion, setEsquemaVersion] = useState<number | null>(null);

  useEffect(() => {
    // Dato informativo, no crítico: si falla, se omite el sufijo sin error visible.
    obtenerVersion()
      .then((r) => setEsquemaVersion(r.esquema_version))
      .catch(() => {});
  }, []);

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
          borderRadius: "8px",
          marginBottom: "1rem",
        }}
      >
        <div style={{ display: "flex", alignItems: "flex-end", gap: "1rem" }}>
          <img
            src="/logo-hexagono.png"
            alt="CELDA"
            style={{ width: "112px", height: "112px", border: "1px solid #d0d5dd" }}
          />
          <h1 style={{ fontSize: "2.5rem", margin: 0, lineHeight: 1 }}>CELDA</h1>
        </div>
        <p style={{ margin: 0 }}>
          <sub><i>Catálogo ELectrónico de Datos Académicos - v{__APP_VERSION__}{esquemaVersion !== null ? ` · esquema ${esquemaVersion}` : ""}</i></sub>
        </p>
      </div>
      <p style={{ margin: 0 }}>
        <b>Módulo de Administración</b>
      </p>
      <button onClick={iniciarSesionConGoogle}>
        🔑 Iniciar sesión
      </button>
      <p></p>
      <hr />
      <p style={{ textAlign: "right" }}>
        <sub>
          <a href={URL_MANUAL_ADMIN} target="_blank" rel="noreferrer">
            Manual del administrador
          </a>
        </sub>
      </p>
    </main>
  );
}
