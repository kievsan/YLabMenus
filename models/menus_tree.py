import uuid

from sqlalchemy.orm import relationship
from sqlmodel import SQLModel, Field, Relationship, Column
from pydantic import field_validator
from typing import Optional, List


class BaseModel(SQLModel, table=False):
    title: str
    description: Optional[str] = None


class Menu(BaseModel, table=True):
    __tablename__ = "menus"
    id: str = Field(default=str(uuid.uuid4()), primary_key=True)
    # id: str = Field(default=str(uuid.uuid4()), primary_key=True)
    submenus: List["Submenu"] = Relationship(back_populates="menu", sa_relationship_kwargs={'cascade': 'all,delete'})

    # @field_validator("id", mode='before')
    # def default_id(cls, uuid_str):
    #     return uuid_str or str(uuid.uuid4())

    def dump(self) -> dict:
        return {
            "id": self.id, "title": self.title, "description": self.description,
            "submenus_count": len(self.submenus),
            "dishes_count": sum([len(submenu.dishes) for submenu in self.submenus])
        }

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": "a2eb416c-2245-4526-bb4b-6343d5c5016f",
                "title": "My menu 1",
                "description": "My menu description 1"
            }
        }


class Submenu(BaseModel, table=True):
    __tablename__ = "submenus"
    id: str = Field(default=str(uuid.uuid4()), primary_key=True)
    menu_id: Optional[str] = Field(default=None, foreign_key="menus.id")
    menu: Optional[Menu] = Relationship(sa_relationship=relationship("Menu", back_populates="submenus"))
    dishes: List["Dish"] = Relationship(back_populates="submenu", sa_relationship_kwargs={'cascade': 'all,delete'})

    def dump(self) -> dict:
        return {"id": self.id, "title": self.title, "description": self.description, "dishes_count": len(self.dishes)}

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": "a2eb416c-2245-4526-bb4b-6343d5c5016f",
                "title": "My menu 1",
                "description": "My menu description 1"
            }
        }


class BaseDish(BaseModel, table=False):
    price: str

    def float_price(self):
        return float(self.price.strip(' "').replace(',', '.'))


class Dish(BaseModel, table=True):
    __tablename__ = "dishes"
    id: str = Field(default=str(uuid.uuid4()), primary_key=True)
    price: float
    submenu_id: Optional[str] = Field(default=None, foreign_key="submenus.id")
    submenu: Optional[Submenu] = Relationship(sa_relationship=relationship("Submenu", back_populates="dishes"))

    def dump(self) -> dict:
        return {"id": self.id, "title": self.title, "description": self.description, "price": str(self.price)}

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": "a2eb416c-2245-4526-bb4b-6343d5c5016f",
                "title": "My menu 1",
                "description": "My menu description 1",
                "price": "12.50"
            }
        }
