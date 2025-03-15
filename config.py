import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG")
    FLASK_ENV = os.getenv("FLASK_ENV")
    FLASK_APP = os.getenv("FLASK_APP")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv(
        "SQLALCHEMY_TRACK_MODIFICATIONS", "False"
    ).lower() in ("true", "1")
    CELERY_CONFIG = {
        "broker_url": os.getenv("CELERY_BROKER_URL"),
        "result_backend": os.getenv("CELERY_RESULT_BACKEND"),
        "worker_pool": os.getenv("CELERY_WORKER_POOL"),
        "broker_connection_retry_on_startup": True,
        "worker_concurrency": os.getenv("CELERY_WORKER_CONCURRENCY"),
        "task_acks_late": os.getenv("CELERY_TASK_ACKS_LATE", "False").lower()
        in ("true", "1"),
        "task_reject_on_worker_lost": os.getenv(
            "CELERY_TASK_REJECT_ON_WORKER_LOST", "False"
        ).lower()
        in ("true", "1"),
        "result_serializer": "json",
        "task_serializer": "json",
        "accept_content": ["json"],
        "result_expires": int(os.getenv("CELERY_TASK_RESULT_EXPIRES")),
    }
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
