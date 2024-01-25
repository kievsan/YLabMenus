from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
from sqlmodel import SQLModel, Session, create_engine

from models.menus_tree import Menu, Submenu, Dish
from settings import DSN

engine = create_engine(DSN, echo=True, connect_args={})


def conn():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close_all()
            engine.dispose()


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None

    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_default_database(),
                          document_models=[Menu, Submenu, Dish])

    class Config:
        env_file = ".env"
