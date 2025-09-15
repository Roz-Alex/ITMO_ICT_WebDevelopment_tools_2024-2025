from typing import Optional, List
from datetime import date, datetime
from enum import Enum

from sqlmodel import SQLModel, Field


class Car(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    year: Optional[str] = None
    mileage: Optional[int] = None
    specs: Optional[str] = None