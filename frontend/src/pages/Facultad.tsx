import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  ApiError,
  FacultadResponse,
  GradoResponse,
  listarGradosDeFacultad,
  obtenerFacultad,
} from "../api";
import CabeceraPagina from "../components/CabeceraPagina";

const FUERA_DE_ALCANCE = "Funcionalidad en construcción";

type Estado =
  | { fase: "cargando" }
  | { fase: "error"; mensaje: string }
  | { fase: "no-encontrado" }
  | { fase: "lista"; facultad: FacultadResponse; grados: GradoResponse[] };

export default function Facultad() {
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
    Promise.all([obtenerFacultad(facultadId), listarGradosDeFacultad(facultadId)])
      .then(([facultad, grados]) => setEstado({ fase: "lista", facultad, grados }))
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

  const { facultad, grados } = estado;

  return (
    <main>
      <CabeceraPagina titulo={facultad.nombre}>
        <button onClick={() => navigate(`/universidades/${facultad.universidad_id}`)}>
          Volver al listado
        </button>
      </CabeceraPagina>
      <hr />
      <button disabled title={FUERA_DE_ALCANCE}>Editar</button>
      <hr />
      <table>
        <thead>
          <tr>
            <th>Código</th>
            <th>Nombre</th>
            <th>Estado</th>
            <th></th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {grados.map((grado) => (
            <tr key={grado.id}>
              <td>{grado.codigo}</td>
              <td>{grado.nombre}</td>
              <td>{grado.estado}</td>
              <td>
                <button onClick={() => navigate(`/admin/grados/${grado.id}`)}>Abrir</button>
              </td>
              <td>
                <button onClick={() => navigate(`/admin/grados/${grado.id}/eliminar`)}>
                  Eliminar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <hr />
      <button onClick={() => navigate(`/facultades/${facultad.id}/grados/crear`)}>
        + Crear Grado
      </button>
    </main>
  );
}
