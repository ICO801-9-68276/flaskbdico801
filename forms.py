from wtforms import Form, StringField, IntegerField, EmailField, TextAreaField
from wtforms import validators


class UserForm(Form):
    id = IntegerField("ID")
    nombre = StringField('Nombre', [
        validators.DataRequired(message="El campo nombre es requerido")
    ])
    apaterno = StringField('Apaterno', [
        validators.DataRequired(message="El campo apaterno es requerido")
    ])
    amaterno = StringField('Amaterno', [
        validators.DataRequired(message="El campo amaterno es requerido")
    ])
    edad = IntegerField('Edad', [
        validators.DataRequired(message="La edad es requerida")
    ])
    email = EmailField('Correo', [
        validators.DataRequired(message="El correo es requerido"),
        validators.Email(message="Ingrese un correo válido")
    ])


class MaestrosForm(Form):
    matricula = IntegerField('Matricula', [
        validators.DataRequired(message="La matrícula es requerida"),
        validators.NumberRange(min=1, max=9999999999, message="Ingrese una matrícula válida")
    ])
    nombre = StringField('Nombre', [
        validators.DataRequired(message="El campo es requerido"),
        validators.length(min=3, max=50, message="Ingrese un nombre válido")
    ])
    apellidos = StringField('Apellidos', [
        validators.DataRequired(message="El campo es requerido")
    ])
    especialidad = StringField('Especialidad', [
        validators.DataRequired(message="Ingrese una especialidad válida")
    ])
    email = EmailField('Email', [
        validators.DataRequired(message="El correo es requerido"),
        validators.Email(message="Ingrese un correo válido")
    ])

class CursoForm(Form):
    nombre = StringField('Nombre del curso', [
        validators.DataRequired(message="El nombre del curso es requerido"),
        validators.length(min=3, max=150, message="Ingrese un nombre válido")
    ])
    descripcion = TextAreaField('Descripción', [
        validators.Optional()
    ])

class InscripcionForm(Form):
    alumno_id = IntegerField('Alumno', [
        validators.DataRequired(message="Debes seleccionar un alumno")
    ])
    curso_id = IntegerField('Curso', [
        validators.DataRequired(message="Debes seleccionar un curso")
    ])