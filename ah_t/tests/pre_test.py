from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists

from ah_t.config import settings
from alembic import command
from alembic.config import Config

engine = create_engine(settings.db_test_url)

if not database_exists(engine.url):
    create_database(engine.url)

alembic_cfg = Config("alembic.ini")

with engine.connect() as connection:
    alembic_cfg.attributes["IS_TEST"] = True
    command.upgrade(alembic_cfg, "head")
