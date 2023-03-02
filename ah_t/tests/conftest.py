import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

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
        connection.begin()
        db = sessionmaker(autocommit=False, autoflush=False, bind=connection)()
        yield db
    finally:
        db.close()
    connection.close()


@pytest.fixture
def car_owner(db: Session) -> CarOwner:
    car_owner = CarOwner(name="Bob")
    db.add(car_owner)
    db.commit()
    return car_owner


@pytest.fixture
def car(db: Session, car_owner: CarOwner) -> CarOwner:
    car = Car(
        license_plate="CAT1234", color=ColorEnum.BLUE, model=ModelEnum.CONVERTIBLE, car_owner_id=car_owner.id
    )
    db.add(car)
    db.commit()
    return car
