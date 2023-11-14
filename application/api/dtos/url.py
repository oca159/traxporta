from typing import Optional

from sqlmodel import SQLModel
from infrastructure.db.models.url import UrlBase


class UrlRead(UrlBase):
    id: int


class UrlCreate(SQLModel):
    original: str


class UrlShortenedCreate(SQLModel):
    original: str
    shortcode: str


class UrlUpdate(SQLModel):
    original: Optional[str] = None
    shortcode: Optional[str] = None
