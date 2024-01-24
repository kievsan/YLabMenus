import json
from typing import List

from fastapi import APIRouter, Depends, Path, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel import select

from database.connection import get_session
from models.menus_tree import Dish, BaseModel, BaseDish

dishes_router = APIRouter(prefix=f"/menus", tags=["Dish"])


@dishes_router.post("/{menu_id}/submenus/{submenu_id}/dishes", response_model=Dish)
async def add_menu(dish_data: BaseDish,
                   menu_id: str, submenu_id: str, session=Depends(get_session)) -> json:
    dish = Dish(
        submenu_id=submenu_id,
        title=dish_data.title, description=dish_data.description, price=to_float(dish_data.price)
    )
    session.add(dish)
    session.commit()
    return JSONResponse(content=dish_dump(dish), media_type="application/json", status_code=201)


@dishes_router.get("/{menu_id}/submenus/{submenu_id}/dishes", response_model=List[Dish])
async def get_all_menus(menu_id: str, submenu_id: str, session=Depends(get_session)) -> json:
    statement = select(Dish)
    dish_list = session.exec(statement).all()
    result: list[dict] = [dish_dump(dish) for dish in dish_list if dish.submenu_id == submenu_id]
    return JSONResponse(content=result, media_type="application/json")


@dishes_router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=Dish)
async def get_menu(menu_id: str, submenu_id: str, dish_id: str, session=Depends(get_session)) -> json:
    dish = session.get(Dish, dish_id)
    if dish and dish.submenu_id == submenu_id:
        return JSONResponse(content=dish_dump(dish), media_type="application/json")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")


@dishes_router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=Dish)
async def update_menu(dish_data: BaseDish,
                      menu_id: str, submenu_id: str, dish_id: str, session=Depends(get_session)) -> json:
    dish = session.get(Dish, dish_id)
    if dish and dish.submenu_id == submenu_id:
        dish.title = dish_data.title
        dish.description = dish_data.description
        dish.price = to_float(dish_data.price)
        session.commit()
        return JSONResponse(content=dish_dump(dish), media_type="application/json", status_code=200)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")


@dishes_router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=Dish)
async def delete_menu(menu_id: str, submenu_id: str, dish_id: str, session=Depends(get_session)) -> json:
    dish = session.get(Dish, dish_id)
    if dish and dish.submenu_id == menu_id:
        session.delete(dish)
        session.commit()
        return JSONResponse(
            content={"status": "true", "message": "The dish has been deleted"},
            media_type="application/json", status_code=200)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")


def dish_dump(dish: Dish) -> dict:
    return {"id": dish.id, "title": dish.title, "description": dish.description, "price": str(dish.price)}


def to_float(num: str) -> float:
    return float(num.strip(' "').replace(',', '.'))
