from flask import render_template, request, redirect, url_for, flash
from models import db, Alumnos, Inscripcion
import forms
from . import alumnos_bp

@alumnos_bp.route("/")
def inicio():
    return render_template("bienvenida.html")

@alumnos_bp.route("/index")
def index():
    return redirect(url_for("alumnos.inicio"))

@alumnos_bp.route("/alumnos", methods=["GET", "POST"])
def alumnos():
    create_form = forms.UserForm(request.form)
    alumno = Alumnos.query.all()
    return render_template("alumnos/index.html", form=create_form, alumno=alumno)

@alumnos_bp.route("/alumnos/nuevo", methods=["GET", "POST"])
def alumnos_nuevo():
    create_form = forms.UserForm(request.form)

    if request.method == "POST":
        if not create_form.validate():
            flash("Te faltan datos o hay campos inválidos")
            return render_template("alumnos/crear.html", form=create_form)

        alum = Alumnos(
            nombre=create_form.nombre.data,
            apaterno=create_form.apaterno.data,
            amaterno=create_form.amaterno.data,
            edad=create_form.edad.data,
            email=create_form.email.data
        )
        db.session.add(alum)
        db.session.commit()
        flash("Alumno registrado correctamente")
        return redirect(url_for("alumnos.alumnos"))

    return render_template("alumnos/crear.html", form=create_form)

@alumnos_bp.route("/alumnos/modificar", methods=["GET", "POST"])
def modificar():
    create_form = forms.UserForm(request.form)
    id = request.args.get("id")

    alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
    if not alum1:
        return redirect(url_for("alumnos.alumnos"))

    if request.method == "GET":
        create_form.id.data = alum1.id
        create_form.nombre.data = alum1.nombre
        create_form.apaterno.data = alum1.apaterno
        create_form.amaterno.data = alum1.amaterno
        create_form.edad.data = alum1.edad
        create_form.email.data = alum1.email

    if request.method == "POST":
        if not create_form.validate():
            flash("Te faltan datos o hay campos inválidos")
            return render_template("alumnos/modificar.html", form=create_form)

        alum1.nombre = create_form.nombre.data
        alum1.apaterno = create_form.apaterno.data
        alum1.amaterno = create_form.amaterno.data
        alum1.edad = create_form.edad.data
        alum1.email = create_form.email.data
        db.session.commit()
        flash("Alumno modificado correctamente")
        return redirect(url_for("alumnos.alumnos"))

    return render_template("alumnos/modificar.html", form=create_form)

@alumnos_bp.route('/alumnos/eliminar', methods=['GET', 'POST'])
def eliminar():
    create_form = forms.UserForm(request.form)

    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()

        if not alum1:
            flash("El alumno no existe")
            return redirect(url_for('alumnos.alumnos'))

        create_form.id.data = alum1.id
        create_form.nombre.data = alum1.nombre
        create_form.apaterno.data = alum1.apaterno
        create_form.amaterno.data = alum1.amaterno
        create_form.edad.data = alum1.edad
        create_form.email.data = alum1.email

    if request.method == 'POST':
        id = request.form.get('id')
        alum = Alumnos.query.get_or_404(id)

        inscripciones = Inscripcion.query.filter_by(alumno_id=alum.id).all()
        for inscripcion in inscripciones:
            db.session.delete(inscripcion)

        db.session.delete(alum)
        db.session.commit()

        flash("Alumno eliminado correctamente")
        return redirect(url_for('alumnos.alumnos'))

    return render_template('alumnos/eliminar.html', form=create_form)

@alumnos_bp.route("/alumnos/detalles", methods=["GET", "POST"])
def detalles():
    if request.method == "GET":
        id = request.args.get("id")
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        if not alum1:
            return redirect(url_for("alumnos.alumnos"))

        return render_template(
            "alumnos/detalles.html",
            id=alum1.id,
            nombre=alum1.nombre,
            apaterno=alum1.apaterno,
            amaterno=alum1.amaterno,
            edad=alum1.edad,
            email=alum1.email
        )

    return redirect(url_for("alumnos.alumnos"))