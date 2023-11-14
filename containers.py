import os
from dependency_injector import containers, providers

from settings import Settings
from domain.entities.shortener import URLShortener
from domain.repositories.url import UrlRepository
from domain.services.url import UrlService
from infrastructure.db.session import Database


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=[
        "application",
        "domain",
        "infrastructure"
    ])

    config = providers.Configuration()
    config.from_pydantic(Settings())

    db = providers.Singleton(Database, db_url=config.database.database_url())

    # Entities
    url_shortener = providers.Factory(
        URLShortener,
        shortcode_length=6,
    )

    # Repositories
    url_repository = providers.Factory(
        UrlRepository,
        session=db.provided.session,
    )

    # Services
    url_service = providers.Factory(
        UrlService,
        url_repository=url_repository,
        url_shortener=url_shortener,
    )


