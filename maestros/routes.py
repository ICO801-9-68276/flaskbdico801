from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Maestros
import forms

maestros_bp = Blueprint('maestros_bp', __name__)

@maestros_bp.route("/maestros", methods=["GET", "POST"])
def maestros():
    create_form = forms.MaestrosForm(request.form)
    maestros = Maestros.query.all()
    return render_template("maestros/index.html", form=create_form, maestros=maestros)

@maestros_bp.route("/maestros/nuevo", methods=["GET", "POST"])
def maestros_nuevo():
    create_form = forms.MaestrosForm(request.form)
    if request.method == 'POST':
        maestro = Maestros(
            matricula=create_form.matricula.data,
            nombre=create_form.nombre.data,
            apellidos=create_form.apellidos.data,
            especialidad=create_form.especialidad.data,
            email=create_form.email.data
        )
        db.session.add(maestro)
        db.session.commit()
        return redirect(url_for('maestros_bp.maestros'))
    return render_template("maestros/crear.html", form=create_form)

@maestros_bp.route("/maestros/modificar", methods=['GET', 'POST'])
def maestros_modificar():
    create_form = forms.MaestrosForm(request.form)
    if request.method == 'GET':
        matricula = request.args.get('matricula')
        maestro1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        create_form.matricula.data = maestro1.matricula
        create_form.nombre.data = maestro1.nombre
        create_form.apellidos.data = maestro1.apellidos
        create_form.especialidad.data = maestro1.especialidad
        create_form.email.data = maestro1.email

    if request.method == 'POST':
        matricula = request.args.get('matricula')
        maestro1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        maestro1.matricula = matricula
        maestro1.nombre = create_form.nombre.data
        maestro1.apellidos = create_form.apellidos.data
        maestro1.especialidad = create_form.especialidad.data
        maestro1.email = create_form.email.data
        db.session.add(maestro1)
        db.session.commit()
        return redirect(url_for('maestros_bp.maestros'))
    return render_template("maestros/modificar.html", form=create_form)

@maestros_bp.route('/maestros/eliminar', methods=['GET', 'POST'])
def maestros_eliminar():
    create_form = forms.MaestrosForm(request.form)
    if request.method == 'GET':
        matricula = request.args.get('matricula')
        maestro1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        create_form.matricula.data = maestro1.matricula
        create_form.nombre.data = maestro1.nombre
        create_form.apellidos.data = maestro1.apellidos
        create_form.especialidad.data = maestro1.especialidad
        create_form.email.data = maestro1.email

    if request.method == 'POST':
        matricula = request.form.get('matricula')
        maestro = Maestros.query.get_or_404(matricula)
        db.session.delete(maestro)
        db.session.commit()
        return redirect(url_for('maestros_bp.maestros'))
    return render_template('maestros/eliminar.html', form=create_form)

@maestros_bp.route("/maestros/detalles", methods=['GET', 'POST'])
def maestros_detalles():
    if request.method == 'GET':
        matricula = request.args.get('matricula')
        maestro1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        matricula = request.args.get('matricula')
        nombre = maestro1.nombre
        apellidos = maestro1.apellidos
        especialidad = maestro1.especialidad
        email = maestro1.email

    return render_template(
        'maestros/detalles.html',
        matricula=matricula,
        nombre=nombre,
        apellidos=apellidos,
        especialidad=especialidad,
        email=email
    )