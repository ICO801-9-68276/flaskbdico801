from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from config import DevelopmentConfig
from maestros import maestros_bp
from alumnos import alumnos_bp
from cursos import cursos_bp
from inscripciones import inscripciones_bp
from consultas import consultas_bp
from models import db

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

app.register_blueprint(maestros_bp)
app.register_blueprint(alumnos_bp)
app.register_blueprint(cursos_bp)
app.register_blueprint(inscripciones_bp)
app.register_blueprint(consultas_bp)

db.init_app(app)
csrf = CSRFProtect()
migrate = Migrate(app, db)

if __name__ == '__main__':
    csrf.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()