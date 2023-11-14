from datetime import datetime
from sqlmodel import SQLModel, Field


class UrlBase(SQLModel):
    original: str
    shortcode: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Url(UrlBase, table=True):
    id: int = Field(default=None, primary_key=True)
