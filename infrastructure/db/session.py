from contextlib import contextmanager, AbstractContextManager
from typing import Callable

from sqlmodel import Session, SQLModel, create_engine


class Database:

    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(db_url, echo=False, connect_args={"check_same_thread": False})

    def create_database(self) -> None:
        SQLModel.metadata.create_all(self._engine)

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        with Session(self._engine) as session:
            yield session
