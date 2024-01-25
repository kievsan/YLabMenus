import json
from typing import List

from fastapi import APIRouter, Depends, Path, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlmodel import select

from database.connection import get_session, engine
from models.menus_tree import Dish, BaseDish

dishes_router = APIRouter(prefix=f"/menus", tags=["Dish"])


@dishes_router.post("/{menu_id}/submenus/{submenu_id}/dishes", response_model=Dish)
async def add_dish(dish_data: BaseDish,
                   submenu_id: str, session=Depends(get_session)) -> json:
    dish = Dish(
        submenu_id=submenu_id,
        title=dish_data.title, description=dish_data.description,
        price=dish_data.float_price()
    )
    result = dish.dump()
    session.add(dish)
    session.commit()
    session.close()
    engine.dispose()
    return JSONResponse(content=result, media_type="application/json", status_code=201)


@dishes_router.get("/{menu_id}/submenus/{submenu_id}/dishes", response_model=List[Dish])
async def get_all_dishes(submenu_id: str, session=Depends(get_session)) -> json:
    statement = select(Dish)
    dish_list = session.exec(statement).all()
    result: list[dict] = [dish.dump() for dish in dish_list if dish.submenu_id == submenu_id]
    return JSONResponse(content=result, media_type="application/json")


@dishes_router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=Dish)
async def get_dish(submenu_id: str, dish_id: str, session=Depends(get_session)) -> json:
    dish = session.get(Dish, dish_id)
    if dish and dish.submenu_id == submenu_id:
        return JSONResponse(content=dish.dump(), media_type="application/json")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")


@dishes_router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=Dish)
async def update_dish(dish_data: BaseDish,
                      submenu_id: str, dish_id: str, session=Depends(get_session)) -> json:
    dish = session.get(Dish, dish_id)
    if dish and dish.submenu_id == submenu_id:
        dish.title = dish_data.title
        dish.description = dish_data.description
        dish.price = dish_data.float_price()
        session.commit()
        return JSONResponse(content=dish.dump(), media_type="application/json", status_code=200)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")


@dishes_router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=Dish)
async def delete_dish(submenu_id: str, dish_id: str, session=Depends(get_session)) -> json:
    dish = session.get(Dish, dish_id)
    if dish and dish.submenu_id == submenu_id:
        session.delete(dish)
        session.commit()
        session.refresh(dish)
        result: dict = {"status": "true", "message": "The dish has been deleted"}
        return JSONResponse(content=result, media_type="application/json", status_code=200)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")
