from flask import render_template, request, redirect, url_for, flash
from models import Alumnos, Curso, Maestros
from . import consultas_bp


@consultas_bp.route("/consultas", methods=["GET"])
def consultas():
    alumnos = Alumnos.query.all()
    cursos = Curso.query.all()
    maestros = Maestros.query.all()

    return render_template(
        "consultas/index.html",
        alumnos=alumnos,
        cursos=cursos,
        maestros=maestros
    )


@consultas_bp.route("/consultas/curso-alumnos", methods=["GET"])
def curso_alumnos():
    cursos = Curso.query.all()
    curso_id = request.args.get("curso_id")

    curso = None
    alumnos_inscritos = []

    if curso_id:
        curso = Curso.query.filter_by(id=int(curso_id)).first()
        if curso:
            alumnos_inscritos = curso.alumnos
        else:
            flash("El curso seleccionado no existe")

    return render_template(
        "consultas/curso_alumnos.html",
        cursos=cursos,
        curso=curso,
        alumnos_inscritos=alumnos_inscritos,
        curso_id=curso_id
    )


@consultas_bp.route("/consultas/alumno-cursos", methods=["GET"])
def alumno_cursos():
    alumnos = Alumnos.query.all()
    alumno_id = request.args.get("alumno_id")

    alumno = None
    cursos_inscritos = []

    if alumno_id:
        alumno = Alumnos.query.filter_by(id=int(alumno_id)).first()
        if alumno:
            cursos_inscritos = alumno.cursos
        else:
            flash("El alumno seleccionado no existe")

    return render_template(
        "consultas/alumno_cursos.html",
        alumnos=alumnos,
        alumno=alumno,
        cursos_inscritos=cursos_inscritos,
        alumno_id=alumno_id
    )


@consultas_bp.route("/consultas/maestro-cursos", methods=["GET"])
def maestro_cursos():
    maestros = Maestros.query.all()
    maestro_id = request.args.get("maestro_id")

    maestro = None
    cursos_asignados = []

    if maestro_id:
        maestro = Maestros.query.filter_by(matricula=int(maestro_id)).first()
        if maestro:
            cursos_asignados = maestro.cursos
        else:
            flash("El maestro seleccionado no existe")

    return render_template(
        "consultas/maestro_cursos.html",
        maestros=maestros,
        maestro=maestro,
        cursos_asignados=cursos_asignados,
        maestro_id=maestro_id
    )