from app.models.asignatura_programa import AsignaturaPrograma


def test_sin_asignacion_se_puede_eliminar(client, resultado_aprendizaje):
    resp = client.get(
        f"/api/v1/resultados-aprendizaje/{resultado_aprendizaje.id}/asignaciones"
    )
    assert resp.status_code == 200
    assert resp.json() == {"materias": [], "asignaturas_programa": []}

    resp = client.delete(
        f"/api/v1/resultados-aprendizaje/{resultado_aprendizaje.id}"
    )
    assert resp.status_code == 204

    resp = client.get(
        f"/api/v1/resultados-aprendizaje/{resultado_aprendizaje.id}"
    )
    assert resp.status_code == 404


def test_asignado_a_materia_bloquea_eliminacion(
    client, materia_del_programa, resultado_aprendizaje
):
    resp = client.post(
        f"/api/v1/materias/{materia_del_programa.id}/resultados-aprendizaje",
        json={"resultado_aprendizaje_id": resultado_aprendizaje.id},
    )
    assert resp.status_code == 204

    resp = client.get(
        f"/api/v1/resultados-aprendizaje/{resultado_aprendizaje.id}/asignaciones"
    )
    assert resp.status_code == 200
    assert resp.json() == {"materias": ["Programación I"], "asignaturas_programa": []}

    resp = client.delete(
        f"/api/v1/resultados-aprendizaje/{resultado_aprendizaje.id}"
    )
    assert resp.status_code == 409
    assert "Materia 'Programación I'" in resp.json()["detail"]


def test_asignado_solo_a_asignatura_programa_bloquea_eliminacion(
    client, db_session, materia_del_programa, resultado_aprendizaje
):
    asignatura = AsignaturaPrograma(
        nombre="Programación I",
        curso=1,
        caracter="Básica",
        idioma="Español",
        ects=6,
        semestre_default=1,
        contenido="",
        estado="Activo",
        materia_id=materia_del_programa.id,
    )
    asignatura.resultados_aprendizaje.append(resultado_aprendizaje)
    db_session.add(asignatura)
    db_session.commit()

    resp = client.get(
        f"/api/v1/resultados-aprendizaje/{resultado_aprendizaje.id}/asignaciones"
    )
    assert resp.status_code == 200
    assert resp.json() == {"materias": [], "asignaturas_programa": ["Programación I"]}

    resp = client.delete(
        f"/api/v1/resultados-aprendizaje/{resultado_aprendizaje.id}"
    )
    assert resp.status_code == 409
    assert "AsignaturaPrograma 'Programación I'" in resp.json()["detail"]


def test_tras_desasociar_de_materia_se_puede_eliminar(
    client, materia_del_programa, resultado_aprendizaje
):
    client.post(
        f"/api/v1/materias/{materia_del_programa.id}/resultados-aprendizaje",
        json={"resultado_aprendizaje_id": resultado_aprendizaje.id},
    )

    resp = client.delete(
        f"/api/v1/materias/{materia_del_programa.id}/resultados-aprendizaje/"
        f"{resultado_aprendizaje.id}"
    )
    assert resp.status_code == 204

    resp = client.delete(
        f"/api/v1/resultados-aprendizaje/{resultado_aprendizaje.id}"
    )
    assert resp.status_code == 204
