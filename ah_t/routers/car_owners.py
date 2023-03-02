from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from ah_t.database import get_db
from ah_t.models import CarOwner
from ah_t.schemas import (
    CarOwnerInPartialUpdateSchema,
    CarOwnerInSchema,
    CarOwnerOutSchema,
    CarOwnerPaginationchema,
)

router = APIRouter()


@router.post("/", response_model=CarOwnerOutSchema, status_code=HTTPStatus.CREATED)
async def create_car_owner(
    car_owner_payload: CarOwnerInSchema, db: Session = Depends(get_db)
) -> CarOwnerInSchema:
    car_owner = CarOwner(**car_owner_payload.dict())
    db.add(car_owner)
    db.commit()

    return car_owner


@router.get("/{id}/", response_model=CarOwnerOutSchema)
async def retrieve_car_owner(id: UUID, db: Session = Depends(get_db)) -> CarOwnerInSchema:
    car_owner = db.get(CarOwner, id)

    if car_owner is None:
        raise HTTPException(status_code=404, detail="Car Owner not found")

    return car_owner


@router.patch("/{id}/", response_model=CarOwnerOutSchema)
async def partial_update_car_owner(
    id: UUID, car_owner_payload: CarOwnerInPartialUpdateSchema, db: Session = Depends(get_db)
) -> CarOwnerInSchema:
    car_owner: CarOwner = db.get(CarOwner, id)

    if car_owner is None:
        raise HTTPException(status_code=404, detail="Car Owner not found")

    for k, v in car_owner_payload.dict(exclude_none=True).items():
        setattr(car_owner, k, v)

    db.commit()
    db.refresh(car_owner)

    return car_owner


@router.get("/", response_model=CarOwnerPaginationchema)
async def list_car_owners(
    request: Request, offset: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> CarOwnerPaginationchema:
    count = db.query(CarOwner).count()

    response = {
        "count": count,
        "next": f"{request.url}?limit={limit}&offset={offset+limit}" if offset + limit < count else None,
        "previous": f"{request.url}?limit={limit}&offset={offset-limit}" if offset - limit > 0 else None,
        "results": db.query(CarOwner).offset(offset).limit(limit).all(),
    }

    return response
