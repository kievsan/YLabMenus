import uuid

from sqlmodel import SQLModel, Field, Column, Relationship, JSON
from typing import Optional, List


class BaseModel(SQLModel, table=False):
    id: str = Field(default=str(uuid.uuid4()), primary_key=True)
    title: str
    description: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": "a2eb416c-2245-4526-bb4b-6343d5c5016f",
                "title": "My menu 1",
                "description": "My menu description 1"
            }
        }


class Menu(BaseModel, table=True):
    __tablename__ = "menus"
    submenus: List["Submenu"] = Relationship(back_populates="menu")


class Submenu(BaseModel, table=True):
    __tablename__ = "submenus"
    menu_id: Optional[str] = Field(default=None, foreign_key="menus.id")
    menu: Optional[Menu] = Relationship(back_populates="submenus")
    dishes: List["Dish"] = Relationship(back_populates="submenu")


class Dish(BaseModel, table=True):
    __tablename__ = "dishes"
    id: str = Field(default=str(uuid.uuid4()), primary_key=True)
    price: int
    submenu_id: Optional[str] = Field(default=None, foreign_key="submenus.id")
    submenu: Optional[Submenu] = Relationship(back_populates="dishes")

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": "a2eb416c-2245-4526-bb4b-6343d5c5016f",
                "title": "My menu 1",
                "description": "My menu description 1",
                "price": 12.50
            }
        }
