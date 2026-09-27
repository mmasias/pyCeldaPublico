"""Índice único en `grados.codigo` (issue #148): un `codigo` duplicado
permitió `GIOI` dos veces en producción (distinta Facultad). El esquema de
prueba se crea a mano, sin la restricción del modelo (`Grado.codigo` ya la
lleva desde este mismo fix) -- para poder simular el estado real anterior
al fix, con duplicados ya existentes."""

from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.scripts.migrar_unique_codigo_grado import migrar_unique_codigo_grado


def _sesion_sin_duplicados():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    metadata = MetaData()
    Table(
        "grados", metadata,
        Column("id", Integer, primary_key=True),
        Column("codigo", String(20)),
    )
    metadata.create_all(bind=engine)
    db = sessionmaker(bind=engine)()
    db.execute(text("INSERT INTO grados (codigo) VALUES ('GII'), ('GIOI')"))
    db.commit()
    return db


def _sesion_con_duplicados():
    db = _sesion_sin_duplicados()
    db.execute(text("INSERT INTO grados (codigo) VALUES ('GIOI')"))
    db.commit()
    return db


def test_plan_sin_duplicados_no_escribe_nada():
    db = _sesion_sin_duplicados()
    migrar_unique_codigo_grado(aplicar=False, db=db)
    indices = db.execute(text("PRAGMA index_list(grados)")).fetchall()
    assert indices == []


def test_apply_sin_duplicados_crea_el_indice():
    db = _sesion_sin_duplicados()
    migrar_unique_codigo_grado(aplicar=True, db=db)
    nombres = [fila[1] for fila in db.execute(text("PRAGMA index_list(grados)")).fetchall()]
    assert "ix_grados_codigo" in nombres


def test_apply_es_idempotente():
    db = _sesion_sin_duplicados()
    migrar_unique_codigo_grado(aplicar=True, db=db)
    migrar_unique_codigo_grado(aplicar=True, db=db)  # no debe fallar
    nombres = [fila[1] for fila in db.execute(text("PRAGMA index_list(grados)")).fetchall()]
    assert nombres.count("ix_grados_codigo") == 1


def test_plan_con_duplicados_no_escribe_nada_y_no_aborta():
    db = _sesion_con_duplicados()
    migrar_unique_codigo_grado(aplicar=False, db=db)  # no debe lanzar
    indices = db.execute(text("PRAGMA index_list(grados)")).fetchall()
    assert indices == []


def test_apply_con_duplicados_aborta_sin_crear_el_indice():
    db = _sesion_con_duplicados()
    try:
        migrar_unique_codigo_grado(aplicar=True, db=db)
        assert False, "debía abortar con SystemExit"
    except SystemExit:
        pass
    indices = db.execute(text("PRAGMA index_list(grados)")).fetchall()
    assert indices == []
