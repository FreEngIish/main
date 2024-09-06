from fastapi import FastAPI

from src.db.database import database, engine, metadata


app = FastAPI()

metadata.create_all(engine)


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()
