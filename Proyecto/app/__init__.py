from flask import Flask
import datetime

def create_app():
    app = Flask(__name__)
    app.secret_key = '2005'

    # Definir el filtro datetimeformat
    @app.template_filter('datetimeformat')
    def datetimeformat(value, format="%Y-%m-%dT%H:%M"):
        """Convierte un objeto datetime en un formato ISO compatible con datetime-local."""
        if isinstance(value, datetime.datetime):
            return value.strftime(format)
        return value

    # Importar y registrar las rutas
    from .routes import routes as routes_blueprint
    app.register_blueprint(routes_blueprint)

    return app
