import pytest
from sqlalchemy.exc import DataError, InternalError
from sqlalchemy.orm import Session

from ah_t.constants import ColorEnum, ModelEnum
from ah_t.models import Car, CarOwner


class TestCarOwner:
    def test_model(self, db: Session) -> None:
        car_owner = CarOwner(name="Bob")
        db.add(car_owner)
        db.commit()
        assert car_owner.is_deleted is False
        assert car_owner.sale_opportunity is True


class TestCar:
    def test_model(self, db: Session) -> None:
        car_owner = CarOwner(name="Bob")
        db.add(car_owner)
        db.commit()
        car = Car(car_owner_id=car_owner.id, color=ColorEnum.BLUE, model=ModelEnum.CONVERTIBLE)
        db.add(car)
        db.commit()
        assert car.is_deleted is False
        assert car.color is ColorEnum.BLUE
        assert car.model is ModelEnum.CONVERTIBLE

    def test_set_wrong_color(self, db: Session) -> None:
        car_owner = CarOwner(name="Bob")
        db.add(car_owner)
        db.commit()
        car = Car(car_owner_id=car_owner.id, color="black", model=ModelEnum.CONVERTIBLE)
        db.add(car)
        with pytest.raises(DataError, match='invalid input value for enum colorenum: "black"'):
            db.commit()

    def test_set_wrong_model(self, db: Session) -> None:
        car_owner = CarOwner(name="Bob")
        db.add(car_owner)
        db.commit()
        car = Car(car_owner_id=car_owner.id, color=ColorEnum.BLUE, model="New model")
        db.add(car)
        with pytest.raises(DataError, match='invalid input value for enum modelenum: "New model"'):
            db.commit()

    def test_car_owner_can_just_have_3_cars(self, db: Session) -> None:
        car_owner = CarOwner(name="Bob")
        db.add(car_owner)
        db.commit()
        for _ in range(4):
            car = Car(car_owner_id=car_owner.id, color=ColorEnum.BLUE, model=ModelEnum.CONVERTIBLE)
            db.add(car)
        with pytest.raises(InternalError, match="Limit quantity car reached"):
            db.commit()

    def test_car_multiples_owner_can_have_3_cars(self, db: Session) -> None:
        for _ in range(4):
            car_owner = CarOwner(name="Bob")
            db.add(car_owner)
            db.commit()
            for _ in range(3):
                car = Car(car_owner_id=car_owner.id, color=ColorEnum.BLUE, model=ModelEnum.CONVERTIBLE)
                db.add(car)
        db.commit()
