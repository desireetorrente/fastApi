from fastapi import FastAPI
from infrastructure import routes as api

import asyncio

background_tasks = set()

async def sleeper(msg: str):
    print("start sleep")
    await asyncio.sleep(20)
    print("end")
    print(msg)

async def connect():
    print("background task")

    task = asyncio.create_task(sleeper(msg="testing background task"))

    # Add task to the set. This creates a strong reference.
    background_tasks.add(task)

    # To prevent keeping references to finished tasks forever,
    # make each task remove its own reference from the set after
    # completion:
    task.add_done_callback(background_tasks.discard)

class AppBuilder:
    __app: FastAPI

    def boot(self) -> FastAPI:
        self.__app = FastAPI()
        self.__app.include_router(api.router)

        self.__app.on_event("startup")(connect)

        return self.__app

app = AppBuilder().boot()
