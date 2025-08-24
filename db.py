import uuid
from typing import Annotated

from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine, Field

from settings import DATABASE_URL


class Operation(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, index=True, default_factory=uuid.uuid4)
    a: float
    b: float
    operator: str = Field(max_length=2)


engine = create_engine(DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


SessionType = Annotated[Session, Depends(get_session)]
