import json
from typing import List

from fastapi import APIRouter, Path, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlmodel import select

from database.connection import get_session, engine
from models.menus_tree import Submenu, BaseModel

submenus_router = APIRouter(prefix=f"/menus", tags=["Submenu"])


@submenus_router.post("/{menu_id}/submenus", response_model=Submenu)
async def add_menu(submenu_data: BaseModel,
                   menu_id: str, session=Depends(get_session)) -> json:
    submenu = Submenu(menu_id=menu_id, title=submenu_data.title, description=submenu_data.description)
    result = submenu.dump()
    session.add(submenu)
    session.commit()
    session.close()
    engine.dispose()
    return JSONResponse(content=result, media_type="application/json", status_code=201)


@submenus_router.get("/{menu_id}/submenus", response_model=List[Submenu])
async def get_all_menus(menu_id: str, session=Depends(get_session)) -> json:
    statement = select(Submenu)
    submenu_list = session.exec(statement).all()
    result: list[dict] = [submenu.dump() for submenu in submenu_list if submenu.menu_id == menu_id]
    return JSONResponse(content=result, media_type="application/json")


@submenus_router.get("/{menu_id}/submenus/{submenu_id}", response_model=Submenu)
async def get_menu(menu_id: str, submenu_id: str, session=Depends(get_session)) -> json:
    submenu = session.get(Submenu, submenu_id)
    if submenu and submenu.menu_id == menu_id:
        return JSONResponse(content=submenu.dump(), media_type="application/json")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")


@submenus_router.patch("/{menu_id}/submenus/{submenu_id}", response_model=Submenu)
async def update_menu(submenu_data: BaseModel,
                      menu_id: str, submenu_id: str, session=Depends(get_session)) -> json:
    submenu = session.get(Submenu, submenu_id)
    if submenu and submenu.menu_id == menu_id:
        submenu.title = submenu_data.title
        submenu.description = submenu_data.description
        session.commit()
        return JSONResponse(content=submenu.dump(), media_type="application/json", status_code=200)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")


@submenus_router.delete("/{menu_id}/submenus/{submenu_id}", response_model=Submenu)
async def delete_menu(menu_id: str, submenu_id: str, session=Depends(get_session)) -> json:
    submenu = session.get(Submenu, submenu_id)
    if submenu and submenu.menu_id == menu_id:
        session.delete(submenu)
        session.commit()
        return JSONResponse(
            content={"status": "true", "message": "The submenu has been deleted"},
            media_type="application/json", status_code=200)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
