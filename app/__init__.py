from flask import Flask
from app.extensions import db, migrate
from app.models import * 
from celery import Celery
from app.routes.main_routes import routes


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config["CELERY_CONFIG"].get("broker_url"),
        backend=app.config["CELERY_CONFIG"].get("result_backend"),
        include=["app.tasks"]
    )
    celery.conf.update(app.config["CELERY_CONFIG"])
    return celery

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(routes)

    celery = make_celery(app)

    return app, celery
