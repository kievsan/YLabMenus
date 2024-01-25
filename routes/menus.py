import json
from typing import List

from fastapi import APIRouter, Path, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlmodel import select

from database.connection import get_session, engine
from models.menus_tree import Menu, BaseModel

menus_router = APIRouter(prefix=f"/menus", tags=["Menu"])


@menus_router.post("/", response_model=Menu)
async def add_menu(menu_data: BaseModel,
                   session=Depends(get_session)) -> json:
    # session.expire_all()
    menu = Menu(title=menu_data.title, description=menu_data.description)
    result = menu.dump()

    session.add(menu)
    session.commit()

    session.close()
    engine.dispose()
    return JSONResponse(content=result, media_type="application/json", status_code=201)


@menus_router.get("/", response_model=List[Menu])
async def get_all_menus(session=Depends(get_session)) -> json:
    statement = select(Menu)
    menu_list = session.exec(statement).all()
    result: list[dict] = [menu.dump() for menu in menu_list]
    return JSONResponse(content=result, media_type="application/json")


@menus_router.get("/{menu_id}", response_model=Menu)
async def get_menu(menu_id: str = Path(..., title="ID to retrieve"),
                   session=Depends(get_session)) -> json:
    menu = session.get(Menu, menu_id)
    if menu:
        session.refresh(menu)
        return JSONResponse(content=menu.dump(), media_type="application/json")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")


@menus_router.patch("/{menu_id}", response_model=Menu)
async def update_menu(menu_data: BaseModel,
                      menu_id: str = Path(..., title="ID to patch"),
                      session=Depends(get_session)) -> json:
    menu = session.get(Menu, menu_id)
    if menu:
        menu.title = menu_data.title
        menu.description = menu_data.description
        session.commit()
        session.refresh(menu)
        return JSONResponse(content=menu.dump(), media_type="application/json", status_code=200)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")


@menus_router.delete("/{menu_id}", response_model=Menu)
async def delete_menu(menu_id: str, session=Depends(get_session)) -> json:
    menu = session.get(Menu, menu_id)
    if menu:
        session.delete(menu)
        session.commit()
        session.refresh(menu)
        return JSONResponse(
            content={"status": "true", "message": "The menu has been deleted"},
            media_type="application/json", status_code=200
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
