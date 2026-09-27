import { API_BASE } from "../api";
import { URL_MANUAL_ADMIN } from "../manualUsuario";

export default function AdminLogin() {
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
            alt="Celda"
            style={{ width: "112px", height: "112px", border: "1px solid #d0d5dd" }}
          />
          <h1 style={{ fontSize: "2.5rem", margin: 0, lineHeight: 1 }}>Celda</h1>
        </div>
        <p style={{ margin: 0 }}>
          <sub><i>Compendio Electrónico Ligero de Datos Académicos</i></sub>
        </p>
      </div>
      <p style={{ margin: 0 }}>
        <b>Módulo de Administración</b>
      </p>      
      <button onClick={iniciarSesionConGoogle}>
        Iniciar sesión con Google
      </button>
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
