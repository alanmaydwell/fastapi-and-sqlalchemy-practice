from .database import get_table_data
from .db_models import Creatures
# Type hints
from sqlalchemy.orm.session import Session


def get_creatures(database: Session) -> list[dict]:
    return get_table_data("creatures", database)


def get_creature(id: int, database: Session) -> Creatures | None:
    response = None
    result = database.query(Creatures).filter_by(id = id).first()
    if result is not None:
        response = {key: getattr(result, key) for key in ("id", "name") }
    return response


def add_creature(name: str, database: Session, commit: bool = True) -> int:
    creature = Creatures(name=name)
    database.add(creature)
    if commit:
        database.commit()
    return creature.id

        
def delete_creature(id: int, database: Session, commit: bool = True) -> int:
    rowcount = database.query(Creatures).filter_by(id = id).delete()
    if commit:
        database.commit()    
    return rowcount


def nuke_creatures(database: Session) -> int:
    rowcount = database.query(Creatures).delete()
    database.commit()
    return rowcount
