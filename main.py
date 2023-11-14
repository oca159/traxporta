try:
  import unzip_requirements
except ImportError:
  pass

from fastapi import FastAPI
from mangum import Mangum

from application.api.routers import urls
from containers import Container


def create_app() -> FastAPI:
    container = Container()

    db = container.db()
    db.create_database()

    app = FastAPI(title='Url shortener API')
    app.container = container
    app.include_router(urls.router)

    return app


app = create_app()

handler = Mangum(app)
