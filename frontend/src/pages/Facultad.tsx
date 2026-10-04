import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  ApiError,
  FacultadResponse,
  ProgramaResponse,
  listarProgramasDeFacultad,
  obtenerFacultad,
} from "../api";
import CabeceraPagina from "../components/CabeceraPagina";
import { useFondoModoAdmin } from "../useFondoModoAdmin";

const FUERA_DE_ALCANCE = "Funcionalidad en construcción";

type Estado =
  | { fase: "cargando" }
  | { fase: "error"; mensaje: string }
  | { fase: "no-encontrado" }
  | { fase: "lista"; facultad: FacultadResponse; programas: ProgramaResponse[] };

export default function Facultad() {
  useFondoModoAdmin();

  const { id } = useParams();
  const navigate = useNavigate();
  const [estado, setEstado] = useState<Estado>({ fase: "cargando" });

  useEffect(() => {
    const facultadId = Number(id);
    if (!Number.isInteger(facultadId) || facultadId <= 0) {
      setEstado({ fase: "no-encontrado" });
      return;
    }
    setEstado({ fase: "cargando" });
    Promise.all([obtenerFacultad(facultadId), listarProgramasDeFacultad(facultadId)])
      .then(([facultad, programas]) => setEstado({ fase: "lista", facultad, programas }))
      .catch((error) => {
        if (error instanceof ApiError && (error.status === 401 || error.status === 403)) {
          navigate("/admin/login", { replace: true });
          return;
        }
        if (error instanceof ApiError && error.status === 404) {
          setEstado({ fase: "no-encontrado" });
          return;
        }
        setEstado({
          fase: "error",
          mensaje: error instanceof Error ? error.message : "Error inesperado",
        });
      });
  }, [id, navigate]);

  if (estado.fase === "cargando") return <p>Cargando...</p>;
  if (estado.fase === "no-encontrado") return <p className="error">Facultad no encontrada</p>;
  if (estado.fase === "error") return <p className="error">Error: {estado.mensaje}</p>;

  const { facultad, programas } = estado;

  return (
    <main>
      <CabeceraPagina titulo={facultad.nombre}>
        <button onClick={() => navigate(`/universidades/${facultad.universidad_id}`)}>
          Volver a la <b>Universidad</b>
        </button>
      </CabeceraPagina>
      <hr />
      <button disabled title={FUERA_DE_ALCANCE}>✏️ Editar</button>
      <hr />
      <button onClick={() => navigate(`/facultades/${facultad.id}/programas/crear`)}>
        ➕ Crear Programa
      </button>
      <table className="jerarquica">
        <thead>
          <tr>
            <th>Código</th>
            <th>Nombre</th>
            <th className="celda-centrada">Estado</th>
            <th className="celda-botones"></th>
            <th className="celda-botones"></th>
          </tr>
        </thead>
        <tbody>
          {programas.map((programa) => (
            <tr key={programa.id}>
              <td>{programa.codigo}</td>
              <td>{programa.nombre}</td>
              <td className="celda-centrada">{programa.estado}</td>
              <td className="celda-botones">
                <button onClick={() => navigate(`/admin/programas/${programa.id}`)}>📂 Abrir</button>
              </td>
              <td className="celda-botones">
                <button onClick={() => navigate(`/admin/programas/${programa.id}/eliminar`)}>
                  🗑️ Eliminar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
