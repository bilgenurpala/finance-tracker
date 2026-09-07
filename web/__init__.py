from flask import Flask, redirect, url_for
from flask_jwt_extended import JWTManager

from settings import settings


def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = settings.secret_key.get_secret_value()
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False

    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def unauthorized_callback(reason):
        return redirect(url_for("main.login"))

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        return redirect(url_for("main.login"))

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return redirect(url_for("main.login"))

    from web.routes import main
    app.register_blueprint(main)

    return app
