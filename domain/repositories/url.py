from contextlib import AbstractContextManager
from typing import Callable, List, Union

from sqlmodel import Session, select

from application.api.dtos.url import UrlUpdate, UrlShortenedCreate
from domain.errors import NotFoundError
from infrastructure.db.models.url import Url


class UrlNotFoundError(NotFoundError):
    entity_name: str = "Url"


class UrlRepository:
    def __init__(self, session: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session = session

    def get_urls(self) -> List[Url]:
        with self.session() as session:
            urls = session.exec(select(Url)).all()
            return urls

    def get_url_by_id(self, url_id: int) -> Union[Url, None]:
        with self.session() as session:
            url = session.get(Url, url_id)
            if not url:
                raise UrlNotFoundError(url_id)
            return url

    def get_url_by_shortcode(self, shortcode: str) -> Union[Url, None]:
        with self.session() as session:
            statement = select(Url).where(Url.shortcode == shortcode)
            result = session.exec(statement).first()
            if not result:
                raise UrlNotFoundError(shortcode)
            return result

    def create_url(self, url: UrlShortenedCreate) -> Url:
        with self.session() as session:
            url = Url.from_orm(url)
            session.add(url)
            session.commit()
            session.refresh(url)
            return url

    def update_url(self, url_id: int, url: UrlUpdate) -> Url:
        with self.session() as session:
            db_url = session.get(Url, url_id)
            if not db_url:
                raise UrlNotFoundError(url_id)
            url_data = url.dict(exclude_unset=True)
            for key, value in url_data.items():
                setattr(db_url, key, value)
            session.add(db_url)
            session.commit()
            session.refresh(db_url)
            return db_url

    def delete_url(self, url_id: int) -> None:
        with self.session() as session:
            url = session.get(Url, url_id)
            if not url:
                raise UrlNotFoundError(url_id)
            session.delete(url)
            session.commit()
