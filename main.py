import asyncio
from typing import List, Union, Type

from sqlalchemy import select
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from asyncpg.exceptions import PostgresError

from init_db import async_session, init_db
from models import Data1, Data2, Data3, DataOut

app = FastAPI()


@app.on_event('startup')
async def init():
    await init_db()


async def query_source(source: Type[Union[Data1, Data2, Data3]]) -> List[Union[Data1, Data2, Data3]]:
    try:
        async with async_session.begin() as session:
            query = await session.execute(select(source))
            data_from_source = query.scalars().all()
            return data_from_source
    except PostgresError as e:
        print(f'Error querying source {source.name}: {e}')
        return []


@app.get('/data/')
async def get_data() -> JSONResponse:
    tasks = [query_source(source) for source in [Data1, Data2, Data3]]
    done, pending = await asyncio.wait(tasks, timeout=2)
    all_source_data = [task.result() for task in done if task.result()]
    validated_data = [DataOut(id=row.id, name=row.name) for source_data in all_source_data for row in source_data]
    sorted_data = sorted(jsonable_encoder(validated_data), key=lambda obj: obj['id'])

    return JSONResponse(sorted_data)
