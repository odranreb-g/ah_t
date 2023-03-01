from uuid import UUID, uuid4

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, String, Uuid
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .constants import ColorEnum, ModelEnum
from .database import Base


def generate_uuid() -> UUID:
    return uuid4()


class CarOwner(Base):
    __tablename__ = "car_owners"

    id = Column(Uuid, primary_key=True, nullable=False, comment="public | id field", default=generate_uuid)
    sale_opportunity = Column(
        Boolean, default=True, nullable=False, comment="private | if person has not car"
    )
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="private | created_at")
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
        comment="private | updated_at",
    )

    is_deleted = Column(Boolean, default=False, nullable=False, comment="private | store if row was deleted")
    name = Column(String, nullable=False, comment="public | car owner name")

    cars = relationship("Car", back_populates="car_owner")


class Car(Base):
    __tablename__ = "cars"

    id = Column(Uuid, primary_key=True, nullable=False, default=generate_uuid)
    car_owner_id = Column(
        Uuid, ForeignKey("car_owners.id"), nullable=False, comment="public | owner_id information"
    )

    color = Column(
        "color", Enum(ColorEnum, create_constraint=True), nullable=False, comment="public | color information"
    )
    model = Column(
        "model",
        Enum(ModelEnum, create_constraint=True),
        nullable=False,
        comment="public | model information",
    )

    car_owner = relationship("CarOwner", back_populates="cars")

    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="private | created_at")
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
        comment="private | updated_at",
    )
    is_deleted = Column(Boolean, default=False, nullable=False, comment="private | store if row was deleted")
