import pytest
from sqlalchemy import Engine, create_engine

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
    def test_model(self, db):
        car_owner = CarOwner()
        db.add(car_owner)
        db.commit()
        assert car_owner.is_deleted is False
        assert car_owner.sale_opportunity is True


class TestCar:
    def test_model(self, db):
        car_owner = CarOwner()
        db.add(car_owner)
        db.commit()
        car = Car(car_owner_id=car_owner.id, color=ColorEnum.BLUE, model=ModelEnum.CONVERTIBLE)
        db.add(car)
        db.commit()
        assert car.is_deleted is False
        assert car.color is ColorEnum.BLUE
        assert car.model is ModelEnum.CONVERTIBLE
