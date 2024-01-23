import json
from typing import List

from fastapi import APIRouter, Path, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlmodel import select

from database.connection import get_session
from models.menus_tree import Menu, Submenu, Dish

dishes_router = APIRouter(prefix=f"/menus", tags=["Dish"])


def dish_dump(dish: Dish) -> dict:
    return {
        "id": dish.id,
        "title": dish.title,
        "description": dish.description,
        "price": dish.price
    }


@dishes_router.post("/{menu_id}/submenus/{submenu_id}/dishes", response_model=Submenu)
async def add_menu(dish_data: Dish, menu_id: str, submenu_id: str, session=Depends(get_session)) -> json:
    session.add(dish_data)
    dish_data.submenu_id = submenu_id
    session.commit()
    session.refresh(dish_data)
    return JSONResponse(
        content=dish_data.model_dump(),
        media_type="application/json",
        status_code=201
    )


@dishes_router.get("/{menu_id}/submenus/{submenu_id}/dishes", response_model=List[Submenu])
async def get_all_menus(menu_id: str, submenu_id: str, session=Depends(get_session)) -> json:
    statement = select(Dish)
    dish_list = session.exec(statement).all()
    result: list[dict] = [dish.model_dump() for dish in dish_list if dish.menu_id == submenu_id]
    return JSONResponse(
        content=result,
        media_type="application/json"
    )


@dishes_router.get("/{menu_id}/submenus/{submenu_id}/dishes{dish_id}", response_model=Submenu)
async def get_menu(menu_id: str, submenu_id: str, dish_id: str, session=Depends(get_session)) -> json:
    dish = session.get(Dish, submenu_id)
    if dish and dish.submenu_id == submenu_id:
        return JSONResponse(
            content=dish.model_dump(),
            media_type="application/json"
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="dish not found"
    )


@dishes_router.patch("/{menu_id}/submenus/{submenu_id}/dishes{dish_id}", response_model=Submenu)
async def update_menu(dish_data: Dish, menu_id: str, submenu_id: str, dish_id: str,
                      session=Depends(get_session)) -> json:
    dish = session.get(Dish, dish_id)
    if dish and dish.submenu_id == submenu_id:
        dish.title = dish_data.title
        dish.description = dish_data.description
        session.commit()
        session.refresh(dish)
        return JSONResponse(
            content=dish_dump(dish),
            media_type="application/json",
            status_code=200
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="dish not found"
    )


@dishes_router.delete("/{menu_id}/submenus/{submenu_id}/dishes{dish_id}", response_model=Submenu)
async def delete_menu(menu_id: str, submenu_id: str, dish_id: str, session=Depends(get_session)) -> json:
    dish = session.get(Dish, dish_id)
    if dish and dish.submenu_id == menu_id:
        session.delete(dish)
        session.commit()
        return JSONResponse(
            content={"status": "true", "message": "The dish has been deleted"},
            media_type="application/json",
            status_code=200
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="dish not found"
    )
