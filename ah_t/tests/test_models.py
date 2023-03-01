import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import DataError, InternalError

from ah_t.config import settings
from ah_t.constants import ColorEnum, ModelEnum
from ah_t.database import sessionmaker
from ah_t.models import Car, CarOwner


@pytest.fixture(scope="session")
def engine_fixture() -> Engine:
    return create_engine(settings.db_test_url)


@pytest.fixture
def db(engine_fixture: Engine):
    connection = engine_fixture.connect()
    try:
        transaction = connection.begin()
        db = sessionmaker(autocommit=False, autoflush=False, bind=connection)()
        yield db
    finally:
        db.close()
        transaction.rollback()
    connection.close()


class TestCarOwner:
    def test_model(self, db) -> None:
        car_owner = CarOwner()
        db.add(car_owner)
        db.commit()
        assert car_owner.is_deleted is False
        assert car_owner.sale_opportunity is True


class TestCar:
    def test_model(self, db) -> None:
        car_owner = CarOwner()
        db.add(car_owner)
        db.commit()
        car = Car(car_owner_id=car_owner.id, color=ColorEnum.BLUE, model=ModelEnum.CONVERTIBLE)
        db.add(car)
        db.commit()
        assert car.is_deleted is False
        assert car.color is ColorEnum.BLUE
        assert car.model is ModelEnum.CONVERTIBLE

    def test_set_wrong_color(self, db) -> None:
        car_owner = CarOwner()
        db.add(car_owner)
        db.commit()
        car = Car(car_owner_id=car_owner.id, color="black", model=ModelEnum.CONVERTIBLE)
        db.add(car)
        with pytest.raises(DataError, match='invalid input value for enum colorenum: "black"'):
            db.commit()

    def test_set_wrong_model(self, db) -> None:
        car_owner = CarOwner()
        db.add(car_owner)
        db.commit()
        car = Car(car_owner_id=car_owner.id, color=ColorEnum.BLUE, model="New model")
        db.add(car)
        with pytest.raises(DataError, match='invalid input value for enum modelenum: "New model"'):
            db.commit()

    def test_car_owner_can_just_have_3_cars(self, db) -> None:
        car_owner = CarOwner()
        db.add(car_owner)
        db.commit()
        for _ in range(4):
            car = Car(car_owner_id=car_owner.id, color=ColorEnum.BLUE, model=ModelEnum.CONVERTIBLE)
            db.add(car)
        with pytest.raises(InternalError, match="Limit quantity car reached"):
            db.commit()

    def test_car_multiples_owner_can_have_3_cars(self, db) -> None:
        for _ in range(4):
            car_owner = CarOwner()
            db.add(car_owner)
            db.commit()
            for _ in range(3):
                car = Car(car_owner_id=car_owner.id, color=ColorEnum.BLUE, model=ModelEnum.CONVERTIBLE)
                db.add(car)
        db.commit()
