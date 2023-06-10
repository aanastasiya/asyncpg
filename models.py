from pydantic import BaseModel
from sqlalchemy import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class DataOut(BaseModel):
    id: int
    name: str


class Base(DeclarativeBase):
    pass


class Data1(Base):
    __tablename__ = "data_1"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))


class Data2(Base):
    __tablename__ = "data_2"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))


class Data3(Base):
    __tablename__ = "data_3"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))
