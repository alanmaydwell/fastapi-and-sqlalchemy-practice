from .database import get_table_data
# Type hints
from sqlalchemy.orm.session import Session


def get_creatures(database: Session) -> list[dict]:
    return get_table_data("creatures", database)
