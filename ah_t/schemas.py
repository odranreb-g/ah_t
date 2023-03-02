from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from ah_t.constants import ColorEnum, ModelEnum


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


class CarInSchema(BaseModel):
    car_owner: UUID
    model: ModelEnum
    color: ColorEnum
    license_plate: str = Field(min_length=7, max_length=7)


class CarInPartialUpdateSchema(BaseModel):
    car_owner: UUID = None
    license_plate: str | None = Field(min_length=7, max_length=7)


class CarOutSchema(BaseModel):
    id: UUID
    car_owner: CarOwnerOutSchema
    model: str
    color: str
    license_plate: str

    class Config:
        orm_mode = True


class BasePagination(BaseModel):
    count: int
    next: str | None
    previous: str | None


class CarOwnerPaginationchema(BasePagination):
    results: list[CarOwnerOutSchema]


class CarPaginationchema(BasePagination):
    results: list[CarOutSchema]
