import os
import json

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from models import Base

load_dotenv()
async_engine = create_async_engine(
    f'postgresql+asyncpg://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@localhost:5432/{os.getenv("DB_NAME")}',
    echo=True
)

async_session = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)


async def init_db():
    with open('data/data.json') as file:
        initial_data = json.load(file)

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text('''
            CREATE TABLE IF NOT EXISTS data_1 (
                id INT PRIMARY KEY,
                name VARCHAR(255)
            )
        '''))
        await conn.execute(text('''
            CREATE TABLE IF NOT EXISTS data_2 (
                id INT PRIMARY KEY,
                name VARCHAR(255)
            )
        '''))
        await conn.execute(text('''
            CREATE TABLE IF NOT EXISTS data_3 (
                id INT PRIMARY KEY,
                name VARCHAR(255)
            );
        '''))

        await conn.execute(text('''
            INSERT INTO data_1 (id, name) VALUES (:id, :name)
        '''), initial_data['source1'])
        await conn.execute(text('''
            INSERT INTO data_2 (id, name) VALUES (:id, :name)
        '''), initial_data['source2'])
        await conn.execute(text('''
            INSERT INTO data_3 (id, name) VALUES (:id, :name)
        '''), initial_data['source3'])
