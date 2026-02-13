from wtforms import form
from wtforms import StringField, IntegerField, EmailField, PasswordField
from wtforms import validators

class UserForm(form):
    nombre = StringField('Nombre')
    apaterno = StringField('Apaterno')
    amaterno = StringField('Amaterno')
    edad = IntegerField("Edad")
    correo = EmailField('Correo')