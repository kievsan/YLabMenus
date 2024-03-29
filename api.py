from const import API_PATH

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn

from database.connection import conn

from routes.menus import menus_router
from routes.submenus import submenus_router
from routes.dishes import dishes_router

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     conn()
#     yield
#     conn().clear()
#
#
# app = FastAPI(lifespan=lifespan)

app = FastAPI()

app.include_router(menus_router, prefix=f"{API_PATH}")
app.include_router(submenus_router, prefix=f"{API_PATH}")
app.include_router(dishes_router, prefix=f"{API_PATH}")


@app.on_event("startup")
def on_startup():
    conn()


@app.get("/")
async def home():
    return RedirectResponse(url=f"{API_PATH}/menus")


if __name__ == '__main__':
    uvicorn.run("api:app", host="localhost", port=8000, reload=True)
