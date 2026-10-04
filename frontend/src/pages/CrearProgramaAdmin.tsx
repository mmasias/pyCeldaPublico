import { FormEvent, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { ApiError, ProgramaResponse, crearProgramaDeFacultad } from "../api";
import { useFondoModoAdmin } from "../useFondoModoAdmin";

export default function CrearProgramaAdmin() {
  useFondoModoAdmin();

  const { facultadId } = useParams();
  const navigate = useNavigate();

  const [codigo, setCodigo] = useState("");
  const [nombre, setNombre] = useState("");
  const [enviando, setEnviando] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const volver = () => navigate(`/facultades/${facultadId}`);

  const enviar = async (e: FormEvent) => {
    e.preventDefault();
    setEnviando(true);
    setError(null);
    try {
      const programa: ProgramaResponse = await crearProgramaDeFacultad(Number(facultadId), {
        codigo,
        nombre,
      });
      // <<include>> editarPrograma(): tras crear, el Admin queda editando el
      // Programa recién creado -- se necesita el id de la respuesta
      navigate(`/admin/programas/${programa.id}/editar`);
    } catch (err) {
      if (err instanceof ApiError && (err.status === 401 || err.status === 403)) {
        navigate("/admin/login", { replace: true });
        return;
      }
      setError(err instanceof Error ? err.message : "Error inesperado");
      setEnviando(false);
    }
  };

  return (
    <main>
      <h1>CREAR PROGRAMA</h1>
      <hr />
      {error && <p className="error">Error: {error}</p>}
      <form onSubmit={enviar}>
        <p>
          <label>
            <b>Código (*):</b>{" "}
            <input value={codigo} onChange={(e) => setCodigo(e.target.value)} required />
          </label>
        </p>
        <p>
          <label>
            <b>Nombre (*):</b>{" "}
            <input value={nombre} onChange={(e) => setNombre(e.target.value)} required />
          </label>
        </p>
        <p>
          <i>(*) Campo obligatorio</i>
        </p>
        <hr />
        <button type="submit" disabled={enviando}>
          Crear
        </button>{" "}
        <button type="button" onClick={volver}>
          Cancelar
        </button>
      </form>
    </main>
  );
}
