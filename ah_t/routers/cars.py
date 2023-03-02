from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from ah_t.database import get_db
from ah_t.models import Car, CarOwner
from ah_t.schemas import (
    CarInPartialUpdateSchema,
    CarInSchema,
    CarOutSchema,
    CarPaginationchema,
)

router = APIRouter()


@router.post("/", response_model=CarOutSchema, status_code=HTTPStatus.CREATED)
async def create_car(car_payload: CarInSchema, db: Session = Depends(get_db)) -> Car:
    car_owner = db.query(CarOwner).filter(CarOwner.id == car_payload.car_owner).with_for_update().one()

    if db.query(Car).filter(Car.car_owner_id == car_payload.car_owner).count() > 2:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="This person has the maximum amount of cars"
        )

    if db.query(Car).filter(Car.license_plate == car_payload.license_plate).count() == 1:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="This license plate already exist"
        )

    car = Car(
        car_owner_id=car_owner.id,
        color=car_payload.color,
        model=car_payload.model,
        license_plate=car_payload.license_plate,
    )
    db.add(car)
    db.commit()

    return car


@router.get("/{id}/", response_model=CarOutSchema)
async def retrieve_car(id: UUID, db: Session = Depends(get_db)) -> Car:
    car = db.get(Car, id)

    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    return car


@router.patch("/{id}/", response_model=CarOutSchema)
async def partial_update_car(
    id: UUID, car_payload: CarInPartialUpdateSchema, db: Session = Depends(get_db)
) -> Car:
    car: Car = db.get(Car, id)

    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    for k, v in car_payload.dict(exclude_none=True).items():
        setattr(car, k, v)

    db.commit()
    db.refresh(car)

    return car


@router.get("/", response_model=CarPaginationchema)
async def list_car_owners(
    request: Request, offset: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> CarPaginationchema:
    count = db.query(Car).count()

    response = {
        "count": count,
        "next": f"{request.url}?limit={limit}&offset={offset+limit}" if offset + limit < count else None,
        "previous": f"{request.url}?limit={limit}&offset={offset-limit}" if offset - limit > 0 else None,
        "results": db.query(Car).offset(offset).limit(limit).all(),
    }

    return response
