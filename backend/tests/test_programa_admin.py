from app.models.facultad import Facultad
from app.models.programa import Programa
from app.models.profesor import Profesor
from app.models.universidad import Universidad


def _crear_facultad(db_session) -> Facultad:
    universidad = Universidad(nombre="UNEATLANTICO")
    db_session.add(universidad)
    db_session.commit()
    db_session.refresh(universidad)
    facultad = Facultad(
        nombre="Escuela Politécnica Superior", universidad_id=universidad.id
    )
    db_session.add(facultad)
    db_session.commit()
    db_session.refresh(facultad)
    return facultad


def test_listar_programas_de_la_facultad_vacio(client, db_session):
    facultad = _crear_facultad(db_session)
    resp = client.get(f"/api/v1/admin/facultades/{facultad.id}/programas")
    assert resp.status_code == 200
    assert resp.json() == []


def test_listar_programas_de_la_facultad_filtra_por_facultad(client, db_session):
    """Variante Admin de abrirProgramas(): listado anidado bajo Facultad
    (wireframe 'PROGRAMAS -- ESCUELA POLITÉCNICA SUPERIOR'), no global --
    los Programas de otras Facultades no aparecen."""
    facultad = _crear_facultad(db_session)
    otra = Facultad(
        nombre="Otra Facultad", universidad_id=facultad.universidad_id
    )
    db_session.add(otra)
    db_session.commit()
    db_session.refresh(otra)

    db_session.add(
        Programa(
            codigo="GII",
            nombre="Grado en Ingeniería Informática",
            facultad_id=facultad.id,
        )
    )
    db_session.add(
        Programa(
            codigo="GIOI",
            nombre="Grado en Organización Industrial",
            facultad_id=facultad.id,
        )
    )
    db_session.add(
        Programa(
            codigo="GIIAA",
            nombre="Grado en Ingeniería de las Industrias Agrarias",
            facultad_id=otra.id,
        )
    )
    db_session.commit()

    resp = client.get(f"/api/v1/admin/facultades/{facultad.id}/programas")
    assert resp.status_code == 200
    assert len(resp.json()) == 2
    assert all(g["facultad_id"] == facultad.id for g in resp.json())


def test_crear_programa_codigo_y_nombre(client, db_session):
    """crearPrograma(): los dos obligatorios, a diferencia de
    crearAsignatura()/crearUniversidad() que solo pedían un campo.
    facultad_id viaja en la URL, no en el body -- mismo patrón que
    POST /api/v1/universidades/{universidad_id}/facultades."""
    facultad = _crear_facultad(db_session)
    resp = client.post(
        f"/api/v1/admin/facultades/{facultad.id}/programas",
        json={"codigo": "GII", "nombre": "Grado en Ingeniería Informática"},
    )
    assert resp.status_code == 201
    assert resp.json()["codigo"] == "GII"
    assert resp.json()["nombre"] == "Grado en Ingeniería Informática"
    assert resp.json()["estado"] == "Vigente"
    assert resp.json()["facultad_id"] == facultad.id


def test_crear_programa_codigo_duplicado_409(client, db_session):
    """issue #148: codigo sin restricción de unicidad permitió un duplicado
    real en producción (GIOI dos veces, distinta Facultad) -- el rechazo es
    global al catálogo, no por Facultad."""
    facultad = _crear_facultad(db_session)
    otra = Facultad(nombre="Otra Facultad", universidad_id=facultad.universidad_id)
    db_session.add(otra)
    db_session.commit()
    db_session.refresh(otra)

    resp = client.post(
        f"/api/v1/admin/facultades/{facultad.id}/programas",
        json={"codigo": "GIOI", "nombre": "Grado en Organización Industrial"},
    )
    assert resp.status_code == 201

    resp = client.post(
        f"/api/v1/admin/facultades/{otra.id}/programas",
        json={"codigo": "GIOI", "nombre": "Otro con el mismo código"},
    )
    assert resp.status_code == 409
    assert db_session.query(Programa).filter_by(codigo="GIOI").count() == 1


def test_crear_programa_sin_codigo_422(client, db_session):
    facultad = _crear_facultad(db_session)
    resp = client.post(
        f"/api/v1/admin/facultades/{facultad.id}/programas", json={"nombre": "x"}
    )
    assert resp.status_code == 422


def test_crear_programa_sin_nombre_422(client, db_session):
    facultad = _crear_facultad(db_session)
    resp = client.post(
        f"/api/v1/admin/facultades/{facultad.id}/programas", json={"codigo": "GII"}
    )
    assert resp.status_code == 422


def test_obtener_programa_admin(client, db_session):
    programa = Programa(codigo="GII", nombre="Grado en Ingeniería Informática")
    db_session.add(programa)
    db_session.commit()
    db_session.refresh(programa)

    resp = client.get(f"/api/v1/admin/programas/{programa.id}")
    assert resp.status_code == 200
    assert resp.json()["codigo"] == "GII"
    assert resp.json()["nombre"] == "Grado en Ingeniería Informática"


def test_obtener_programa_admin_404(client):
    resp = client.get("/api/v1/admin/programas/999")
    assert resp.status_code == 404


def test_editar_programa(client, db_session):
    programa = Programa(codigo="GII", nombre="Nombre original")
    db_session.add(programa)
    db_session.commit()
    db_session.refresh(programa)

    resp = client.put(
        f"/api/v1/admin/programas/{programa.id}",
        json={"nombre": "Grado en Ingeniería Informática"},
    )
    assert resp.status_code == 200
    assert resp.json()["nombre"] == "Grado en Ingeniería Informática"
    # el codigo no es editable tras la creación -- no viaja en ProgramaUpdate
    assert resp.json()["codigo"] == "GII"


def test_editar_programa_sin_nombre_422(client, db_session):
    programa = Programa(codigo="GII", nombre="x")
    db_session.add(programa)
    db_session.commit()
    db_session.refresh(programa)

    resp = client.put(f"/api/v1/admin/programas/{programa.id}", json={})
    assert resp.status_code == 422


def test_editar_programa_404(client):
    resp = client.put("/api/v1/admin/programas/999", json={"nombre": "x"})
    assert resp.status_code == 404


# --- eliminarPrograma(): borrado lógico, SIN <<choice>> bloqueante -------------


def test_eliminar_programa_pasa_a_extinguido(client, db_session):
    """A diferencia de eliminarFacultad()/eliminarResultadoAprendizaje(),
    aquí no hay rama de bloqueo -- confirmar siempre tiene éxito. El
    endpoint devuelve 200 con el objeto actualizado (no 204): el recurso
    sigue existiendo, solo cambia su estado."""
    programa = Programa(codigo="GIOI", nombre="Grado en Organización Industrial")
    db_session.add(programa)
    db_session.commit()
    db_session.refresh(programa)

    resp = client.delete(f"/api/v1/admin/programas/{programa.id}")
    assert resp.status_code == 200
    assert resp.json()["estado"] == "Extinguido"

    # sigue existiendo -- borrado lógico, no físico
    resp_get = client.get(f"/api/v1/admin/programas/{programa.id}")
    assert resp_get.status_code == 200
    assert resp_get.json()["estado"] == "Extinguido"


def test_eliminar_programa_404(client):
    resp = client.delete("/api/v1/admin/programas/999")
    assert resp.status_code == 404


# --- Directores de Programa desde la vista del Programa (issue #492) --------------
# Complementa test_profesor.py (que ya cubre definirDirectorPrograma()/
# quitarDirectorPrograma() desde la vista del Profesor): aquí se reusan tal
# cual esos mismos endpoints, verificando que ProgramaResponse.directores (y el
# selector nuevo de disponibles) reflejan el resultado esperado desde este
# otro punto de entrada.


def _crear_profesor(db_session, universidad, email, nombre="Dr. Prueba"):
    profesor = Profesor(nombre=nombre, email=email, universidad_id=universidad.id)
    db_session.add(profesor)
    db_session.commit()
    db_session.refresh(profesor)
    return profesor


def _crear_programa_sin_facultad(db_session, codigo="GII", nombre="Grado en Ingeniería Informática"):
    programa = Programa(codigo=codigo, nombre=nombre)
    db_session.add(programa)
    db_session.commit()
    db_session.refresh(programa)
    return programa


def test_obtener_programa_admin_sin_directores_lista_vacia(client, db_session):
    programa = _crear_programa_sin_facultad(db_session)
    resp = client.get(f"/api/v1/admin/programas/{programa.id}")
    assert resp.status_code == 200
    assert resp.json()["directores"] == []


def test_obtener_programa_admin_con_un_director(
    client, db_session, universidad, curso_academico
):
    programa = _crear_programa_sin_facultad(db_session)
    profesor = _crear_profesor(
        db_session, universidad, "directora@uneatlantico.es", "Dra. Directora"
    )

    resp = client.post(
        f"/api/v1/profesores/{profesor.id}/directores-programa",
        json={"programa_id": programa.id},
    )
    assert resp.status_code == 200

    resp = client.get(f"/api/v1/admin/programas/{programa.id}")
    assert resp.status_code == 200
    assert resp.json()["directores"] == [
        {
            "profesor_id": profesor.id,
            "nombre": "Dra. Directora",
            "email": "directora@uneatlantico.es",
        }
    ]


def test_obtener_programa_admin_con_varios_directores(
    client, db_session, universidad, curso_academico
):
    programa = _crear_programa_sin_facultad(db_session)
    uno = _crear_profesor(db_session, universidad, "uno@uneatlantico.es", "Dr. Uno")
    dos = _crear_profesor(db_session, universidad, "dos@uneatlantico.es", "Dr. Dos")

    for profesor in (uno, dos):
        resp = client.post(
            f"/api/v1/profesores/{profesor.id}/directores-programa",
            json={"programa_id": programa.id},
        )
        assert resp.status_code == 200

    resp = client.get(f"/api/v1/admin/programas/{programa.id}")
    ids = {d["profesor_id"] for d in resp.json()["directores"]}
    assert ids == {uno.id, dos.id}


def test_listar_profesores_disponibles_para_dirigir_excluye_los_que_ya_dirigen(
    client, db_session, universidad, curso_academico
):
    """Reverso exacto de listarProgramasDisponiblesParaDirigir(): mismo
    criterio de exclusión, recorrido desde Programa hacia Profesor."""
    programa = _crear_programa_sin_facultad(db_session)
    dirige = _crear_profesor(db_session, universidad, "dirige@uneatlantico.es")
    disponible = _crear_profesor(db_session, universidad, "disponible@uneatlantico.es")

    resp = client.post(
        f"/api/v1/profesores/{dirige.id}/directores-programa",
        json={"programa_id": programa.id},
    )
    assert resp.status_code == 200

    resp = client.get(
        f"/api/v1/admin/programas/{programa.id}/profesores-disponibles-para-dirigir"
    )
    assert resp.status_code == 200
    ids = {p["id"] for p in resp.json()}
    assert dirige.id not in ids
    assert disponible.id in ids


def test_listar_profesores_disponibles_para_dirigir_sin_ninguno_disponible(
    client, db_session, universidad, curso_academico
):
    programa = _crear_programa_sin_facultad(db_session)
    profesor = _crear_profesor(db_session, universidad, "unico@uneatlantico.es")
    client.post(
        f"/api/v1/profesores/{profesor.id}/directores-programa",
        json={"programa_id": programa.id},
    )

    resp = client.get(
        f"/api/v1/admin/programas/{programa.id}/profesores-disponibles-para-dirigir"
    )
    assert resp.status_code == 200
    assert resp.json() == []


def test_listar_profesores_disponibles_para_dirigir_programa_404(client):
    resp = client.get(
        "/api/v1/admin/programas/999/profesores-disponibles-para-dirigir"
    )
    assert resp.status_code == 404


def test_quitar_director_programa_desde_flujo_de_programa_actualiza_directores(
    client, db_session, universidad, curso_academico
):
    """Reusa tal cual DELETE /profesores/{id}/directores-programa/{programa_id}
    -- cero endpoints de escritura nuevos (issue #492)."""
    programa = _crear_programa_sin_facultad(db_session)
    uno = _crear_profesor(db_session, universidad, "uno@uneatlantico.es")
    dos = _crear_profesor(db_session, universidad, "dos@uneatlantico.es")
    for profesor in (uno, dos):
        client.post(
            f"/api/v1/profesores/{profesor.id}/directores-programa",
            json={"programa_id": programa.id},
        )

    resp = client.delete(f"/api/v1/profesores/{uno.id}/directores-programa/{programa.id}")
    assert resp.status_code == 204

    resp = client.get(f"/api/v1/admin/programas/{programa.id}")
    ids = {d["profesor_id"] for d in resp.json()["directores"]}
    assert ids == {dos.id}


def test_quitar_unico_director_programa_desde_flujo_de_programa_409(
    client, db_session, universidad, curso_academico
):
    """La regla de negocio (409 si es el único director) vive en el
    endpoint reusado -- no se duplica aquí, solo se comprueba que sigue
    aplicando desde este flujo."""
    programa = _crear_programa_sin_facultad(db_session)
    profesor = _crear_profesor(db_session, universidad, "unico@uneatlantico.es")
    client.post(
        f"/api/v1/profesores/{profesor.id}/directores-programa",
        json={"programa_id": programa.id},
    )

    resp = client.delete(f"/api/v1/profesores/{profesor.id}/directores-programa/{programa.id}")
    assert resp.status_code == 409

    resp = client.get(f"/api/v1/admin/programas/{programa.id}")
    assert len(resp.json()["directores"]) == 1


def test_editar_programa_con_directores_no_rompe(
    client, db_session, universidad, curso_academico
):
    """Regresión: Programa.directores es una relación ORM real -- ProgramaResponse
    se construye siempre explícito (ProgramaResponse.desde_programa()), nunca vía
    from_attributes directo sobre el Programa, para no intentar leer esa
    relación con la forma equivocada en un Programa que ya tenga directores."""
    programa = _crear_programa_sin_facultad(db_session, nombre="Nombre original")
    profesor = _crear_profesor(db_session, universidad, "director@uneatlantico.es")
    client.post(
        f"/api/v1/profesores/{profesor.id}/directores-programa",
        json={"programa_id": programa.id},
    )

    resp = client.put(
        f"/api/v1/admin/programas/{programa.id}", json={"nombre": "Nombre nuevo"}
    )
    assert resp.status_code == 200
    assert resp.json()["nombre"] == "Nombre nuevo"

    resp = client.delete(f"/api/v1/admin/programas/{programa.id}")
    assert resp.status_code == 200
    assert resp.json()["estado"] == "Extinguido"


def test_listar_programas_de_la_facultad_con_directores_no_rompe(
    client, db_session, facultad, curso_academico
):
    """Mismo caso que test_editar_programa_con_directores_no_rompe() pero para
    el listado -- issue #492 lo deja con directores=[] por defecto (no
    aplica mostrarlos ahí), solo debe no reventar."""
    programa = Programa(codigo="GII", nombre="x", facultad_id=facultad.id)
    db_session.add(programa)
    db_session.commit()
    db_session.refresh(programa)
    profesor = Profesor(
        nombre="Dr. Director",
        email="director@uneatlantico.es",
        universidad_id=facultad.universidad_id,
    )
    db_session.add(profesor)
    db_session.commit()
    db_session.refresh(profesor)
    client.post(
        f"/api/v1/profesores/{profesor.id}/directores-programa",
        json={"programa_id": programa.id},
    )

    resp = client.get(f"/api/v1/admin/facultades/{facultad.id}/programas")
    assert resp.status_code == 200
    assert resp.json()[0]["directores"] == []
