from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CarOwnerInSchema(BaseModel):
    name: str
    is_deleted: bool = False


class CarOwnerInPartialUpdateSchema(BaseModel):
    name: str = None
    is_deleted: bool = None
    sale_opportunity: bool = None


class CarOwnerOutSchema(BaseModel):
    id: UUID
    name: str
    sale_opportunity: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class BasePagination(BaseModel):
    count: int
    next: str | None
    previous: str | None


class CarOwneraginationchema(BasePagination):
    results: list[CarOwnerOutSchema]
