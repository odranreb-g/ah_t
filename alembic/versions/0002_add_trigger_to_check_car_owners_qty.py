"""add_trigger_to_check_car_owners_qty

Revision ID: 0002
Revises: 0001
Create Date: 2023-03-01 12:20:58.827012

"""
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    trg_function = """
    CREATE OR REPLACE FUNCTION trg_can_car_owner_register_a_new_car()
      RETURNS TRIGGER
      LANGUAGE PLPGSQL
      AS
    $$
    BEGIN
            IF (select count(*) from cars where car_owner_id = NEW.car_owner_id) > 2 THEN
                RAISE EXCEPTION 'Limit quantity car reached.';
            END IF;

            RETURN NEW;
    END;
    $$
    """

    trigger = """
    CREATE TRIGGER can_car_owner_register_a_new_car_check
    BEFORE INSERT ON "cars"
    FOR EACH ROW EXECUTE PROCEDURE trg_can_car_owner_register_a_new_car();
    """
    op.execute(trg_function)
    op.execute(trigger)


def downgrade() -> None:
    drop_trigger = "DROP TRIGGER IF EXISTS can_car_owner_register_a_new_car_check ON cars;"
    drop_trg_function = "DROP FUNCTION IF EXISTS trg_can_car_owner_register_a_new_car;"

    op.execute(drop_trigger)
    op.execute(drop_trg_function)
