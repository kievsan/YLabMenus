from typing import Any, List, Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from sqlmodel import SQLModel, Session, create_engine

from models.menus_tree import Menu

engine = create_engine(
    'postgresql://adm:111@127.0.0.1:5431/menu_pgdb',
    echo=True,
    connect_args={}
)


def conn():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None

    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_default_database(),
                          document_models=[Menu])

    class Config:
        env_file = ".env"

