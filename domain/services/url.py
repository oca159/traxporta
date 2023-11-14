from typing import List
from fastapi import HTTPException

from application.api.dtos.url import UrlCreate, UrlUpdate, UrlShortenedCreate
from domain.entities.shortener import URLShortener
from domain.repositories.url import UrlRepository, UrlNotFoundError
from infrastructure.db.models.url import Url


class UrlService:
    def __init__(self, url_repository: UrlRepository, url_shortener: URLShortener) -> None:
        self.url_repository = url_repository
        self.url_shortener = url_shortener

    def get_urls(self) -> List[Url]:
        return self.url_repository.get_urls()

    def get_url_by_id(self, url_id: int) -> Url:
        return self._handle_operation(
            lambda: self.url_repository.get_url_by_id(url_id)
        )

    def get_url_by_shortcode(self, shortcode: str) -> Url:
        return self._handle_operation(
            lambda: self.url_repository.get_url_by_shortcode(shortcode)
        )

    def create_url(self, url: UrlCreate) -> Url:
        shortcode = self.url_shortener.shorten_url(url.original)
        url_shortened = UrlShortenedCreate(original=url.original, shortcode=shortcode)
        new_url = self.url_repository.create_url(url_shortened)
        return new_url

    def update_url(self, url_id: int, url: UrlUpdate) -> Url:
        updated_url = self._handle_operation(
            lambda: self.url_repository.update_url(url_id, url)
        )
        return updated_url

    def delete_url(self, url_id: int) -> None:
        self._handle_operation(
            lambda: self.url_repository.delete_url(url_id)
        )

    def _handle_operation(self, operation):
        try:
            return operation()
        except UrlNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))