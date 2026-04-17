from flask import render_template, request, redirect, url_for, flash
from models import db, Alumnos, Curso, Inscripcion
from . import inscripciones_bp


@inscripciones_bp.route("/inscripciones", methods=["GET"])
def inscripciones():
    inscripciones_lista = Inscripcion.query.all()
    return render_template("inscripciones/index.html", inscripciones=inscripciones_lista)


@inscripciones_bp.route("/inscripciones/nuevo", methods=["GET", "POST"])
def inscripciones_nuevo():
    alumnos = Alumnos.query.all()
    cursos = Curso.query.all()

    if request.method == "POST":
        alumno_id = request.form.get("alumno_id")
        curso_id = request.form.get("curso_id")

        if not alumno_id or not curso_id:
            flash("Debes seleccionar alumno y curso")
            return render_template(
                "inscripciones/crear.html",
                alumnos=alumnos,
                cursos=cursos,
                alumno_id=alumno_id,
                curso_id=curso_id
            )

        alumno = Alumnos.query.filter_by(id=int(alumno_id)).first()
        curso = Curso.query.filter_by(id=int(curso_id)).first()

        if not alumno or not curso:
            flash("El alumno o el curso no existen")
            return render_template(
                "inscripciones/crear.html",
                alumnos=alumnos,
                cursos=cursos,
                alumno_id=alumno_id,
                curso_id=curso_id
            )

        existe_inscripcion = Inscripcion.query.filter(
            Inscripcion.alumno_id == int(alumno_id),
            Inscripcion.curso_id == int(curso_id)
        ).first()

        if existe_inscripcion:
            flash("Ese alumno ya está inscrito en ese curso")
            return render_template(
                "inscripciones/crear.html",
                alumnos=alumnos,
                cursos=cursos,
                alumno_id=alumno_id,
                curso_id=curso_id
            )

        curso.alumnos.append(alumno)
        db.session.commit()
        flash("Inscripción registrada correctamente")
        return redirect(url_for("inscripciones.inscripciones"))

    return render_template(
        "inscripciones/crear.html",
        alumnos=alumnos,
        cursos=cursos,
        alumno_id="",
        curso_id=""
    )


@inscripciones_bp.route("/inscripciones/modificar", methods=["GET", "POST"])
def inscripciones_modificar():
    id = request.args.get("id")
    inscripcion = Inscripcion.query.filter_by(id=id).first()
    alumnos = Alumnos.query.all()
    cursos = Curso.query.all()

    if not inscripcion:
        flash("La inscripción no existe")
        return redirect(url_for("inscripciones.inscripciones"))

    if request.method == "POST":
        alumno_id = request.form.get("alumno_id")
        curso_id = request.form.get("curso_id")

        if not alumno_id or not curso_id:
            flash("Debes seleccionar alumno y curso")
            return render_template(
                "inscripciones/modificar.html",
                inscripcion=inscripcion,
                alumnos=alumnos,
                cursos=cursos,
                alumno_id=alumno_id,
                curso_id=curso_id
            )

        alumno = Alumnos.query.filter_by(id=int(alumno_id)).first()
        curso = Curso.query.filter_by(id=int(curso_id)).first()

        if not alumno or not curso:
            flash("El alumno o el curso no existen")
            return render_template(
                "inscripciones/modificar.html",
                inscripcion=inscripcion,
                alumnos=alumnos,
                cursos=cursos,
                alumno_id=alumno_id,
                curso_id=curso_id
            )

        existe_inscripcion = Inscripcion.query.filter(
            Inscripcion.alumno_id == int(alumno_id),
            Inscripcion.curso_id == int(curso_id),
            Inscripcion.id != inscripcion.id
        ).first()

        if existe_inscripcion:
            flash("Ese alumno ya está inscrito en ese curso")
            return render_template(
                "inscripciones/modificar.html",
                inscripcion=inscripcion,
                alumnos=alumnos,
                cursos=cursos,
                alumno_id=alumno_id,
                curso_id=curso_id
            )

        inscripcion.alumno_id = int(alumno_id)
        inscripcion.curso_id = int(curso_id)
        db.session.commit()
        flash("Inscripción modificada correctamente")
        return redirect(url_for("inscripciones.inscripciones"))

    return render_template(
        "inscripciones/modificar.html",
        inscripcion=inscripcion,
        alumnos=alumnos,
        cursos=cursos,
        alumno_id=inscripcion.alumno_id,
        curso_id=inscripcion.curso_id
    )


@inscripciones_bp.route("/inscripciones/eliminar", methods=["GET", "POST"])
def inscripciones_eliminar():
    id = request.args.get("id")
    inscripcion = Inscripcion.query.filter_by(id=id).first()

    if not inscripcion:
        flash("La inscripción no existe")
        return redirect(url_for("inscripciones.inscripciones"))

    if request.method == "POST":
        db.session.delete(inscripcion)
        db.session.commit()
        flash("Inscripción eliminada correctamente")
        return redirect(url_for("inscripciones.inscripciones"))

    return render_template("inscripciones/eliminar.html", inscripcion=inscripcion)


@inscripciones_bp.route("/inscripciones/detalles", methods=["GET"])
def inscripciones_detalles():
    id = request.args.get("id")
    inscripcion = Inscripcion.query.filter_by(id=id).first()

    if not inscripcion:
        flash("La inscripción no existe")
        return redirect(url_for("inscripciones.inscripciones"))

    return render_template("inscripciones/detalles.html", inscripcion=inscripcion)