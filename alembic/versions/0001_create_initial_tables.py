"""create_initial_tables

Revision ID: 0001
Revises:
Create Date: 2023-03-01 08:17:07.233749

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "car_owners",
        sa.Column("id", sa.Uuid(), nullable=False, comment="public | id field"),
        sa.Column(
            "sale_opportunity", sa.Boolean(), nullable=False, comment="private | if person has not car"
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
            comment="private | created_at",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
            comment="private | updated_at",
        ),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, comment="private | store if row was deleted"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "cars",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("car_owner_id", sa.Uuid(), nullable=False, comment="public | owner_id information"),
        sa.Column(
            "color",
            sa.Enum("YELLOW", "BLUE", "GRAY", name="colorenum", create_constraint=True),
            nullable=False,
            comment="public | color information",
        ),
        sa.Column(
            "model",
            sa.Enum("HATCH", "SEDAN", "CONVERTIBLE", name="modelenum", create_constraint=True),
            nullable=False,
            comment="public | model information",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
            comment="private | created_at",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
            comment="private | updated_at",
        ),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, comment="private | store if row was deleted"),
        sa.ForeignKeyConstraint(
            ["car_owner_id"],
            ["car_owners.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("cars")
    op.drop_table("car_owners")
    # ### end Alembic commands ###
