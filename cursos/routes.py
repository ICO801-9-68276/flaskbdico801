from flask import render_template, request, redirect, url_for, flash
from models import db, Curso, Maestros
import forms
from . import cursos_bp


@cursos_bp.route("/cursos", methods=["GET", "POST"])
def cursos():
    create_form = forms.CursoForm(request.form)
    cursos_lista = Curso.query.all()
    return render_template("cursos/index.html", form=create_form, cursos=cursos_lista)


@cursos_bp.route("/cursos/nuevo", methods=["GET", "POST"])
def cursos_nuevo():
    create_form = forms.CursoForm(request.form)
    maestros = Maestros.query.all()

    if request.method == "POST":
        maestro_id = request.form.get("maestro_id")

        if not create_form.validate():
            flash("Te faltan datos o hay campos inválidos")
            return render_template("cursos/crear.html", form=create_form, maestros=maestros, maestro_id=maestro_id)

        if not maestro_id:
            flash("Debes seleccionar un maestro")
            return render_template("cursos/crear.html", form=create_form, maestros=maestros, maestro_id=maestro_id)

        maestro = Maestros.query.filter_by(matricula=int(maestro_id)).first()
        if not maestro:
            flash("El maestro seleccionado no existe")
            return render_template("cursos/crear.html", form=create_form, maestros=maestros, maestro_id=maestro_id)

        existe_curso = Curso.query.filter(
            Curso.nombre == create_form.nombre.data,
            Curso.maestro_id == int(maestro_id)
        ).first()

        if existe_curso:
            flash("Ya existe un curso con ese nombre para ese maestro")
            return render_template("cursos/crear.html", form=create_form, maestros=maestros, maestro_id=maestro_id)

        curso = Curso(
            nombre=create_form.nombre.data,
            descripcion=create_form.descripcion.data,
            maestro_id=int(maestro_id)
        )
        db.session.add(curso)
        db.session.commit()
        flash("Curso registrado correctamente")
        return redirect(url_for("cursos.cursos"))

    return render_template("cursos/crear.html", form=create_form, maestros=maestros, maestro_id="")


@cursos_bp.route("/cursos/modificar", methods=["GET", "POST"])
def cursos_modificar():
    create_form = forms.CursoForm(request.form)
    maestros = Maestros.query.all()
    id = request.args.get("id")
    curso1 = Curso.query.filter(Curso.id == id).first()

    if not curso1:
        flash("El curso no existe")
        return redirect(url_for("cursos.cursos"))

    if request.method == "GET":
        create_form.nombre.data = curso1.nombre
        create_form.descripcion.data = curso1.descripcion
        return render_template(
            "cursos/modificar.html",
            form=create_form,
            maestros=maestros,
            curso=curso1,
            maestro_id=curso1.maestro_id
        )

    maestro_id = request.form.get("maestro_id")

    if not create_form.validate():
        flash("Te faltan datos o hay campos inválidos")
        return render_template(
            "cursos/modificar.html",
            form=create_form,
            maestros=maestros,
            curso=curso1,
            maestro_id=maestro_id
        )

    if not maestro_id:
        flash("Debes seleccionar un maestro")
        return render_template(
            "cursos/modificar.html",
            form=create_form,
            maestros=maestros,
            curso=curso1,
            maestro_id=maestro_id
        )

    maestro = Maestros.query.filter_by(matricula=int(maestro_id)).first()
    if not maestro:
        flash("El maestro seleccionado no existe")
        return render_template(
            "cursos/modificar.html",
            form=create_form,
            maestros=maestros,
            curso=curso1,
            maestro_id=maestro_id
        )

    existe_curso = Curso.query.filter(
        Curso.nombre == create_form.nombre.data,
        Curso.maestro_id == int(maestro_id),
        Curso.id != curso1.id
    ).first()

    if existe_curso:
        flash("Ya existe un curso con ese nombre para ese maestro")
        return render_template(
            "cursos/modificar.html",
            form=create_form,
            maestros=maestros,
            curso=curso1,
            maestro_id=maestro_id
        )

    curso1.nombre = create_form.nombre.data
    curso1.descripcion = create_form.descripcion.data
    curso1.maestro_id = int(maestro_id)

    db.session.commit()
    flash("Curso modificado correctamente")
    return redirect(url_for("cursos.cursos"))


@cursos_bp.route("/cursos/eliminar", methods=["GET", "POST"])
def cursos_eliminar():
    id = request.args.get("id")
    curso1 = Curso.query.filter(Curso.id == id).first()

    if not curso1:
        flash("El curso no existe")
        return redirect(url_for("cursos.cursos"))

    if request.method == "POST":
        if curso1.alumnos:
            flash("No se puede eliminar el curso porque tiene alumnos inscritos. Debes eliminar primero las inscripciones de esa materia antes de eliminar el curso o debes de cambiar a otro maestro diferente.")
            return render_template("cursos/eliminar.html", curso=curso1)

        db.session.delete(curso1)
        db.session.commit()
        flash("Curso eliminado correctamente")
        return redirect(url_for("cursos.cursos"))

    return render_template("cursos/eliminar.html", curso=curso1)


@cursos_bp.route("/cursos/detalles", methods=["GET"])
def cursos_detalles():
    id = request.args.get("id")
    curso1 = Curso.query.filter(Curso.id == id).first()

    if not curso1:
        flash("El curso no existe")
        return redirect(url_for("cursos.cursos"))

    return render_template("cursos/detalles.html", curso=curso1)