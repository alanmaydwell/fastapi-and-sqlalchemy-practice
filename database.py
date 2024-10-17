import sqlalchemy
from sqlalchemy.orm import sessionmaker
# Type hints below
from collections.abc import Iterable, Hashable
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.schema import MetaData, Table


def get_metadata(database: Session) -> MetaData:
    engine = database.get_bind()
    meta_data = sqlalchemy.MetaData()
    meta_data.reflect(bind=engine)
    return meta_data


def get_table(tablename: str, database: Session) -> Table | None:
    meta_data = get_metadata(database)
    return meta_data.tables.get(tablename, None)


def make_list_of_dicts(headings: list[Hashable], rows: Iterable[Iterable]) -> list[dict]:
    """Created to convert list of column headings and list of row tuples from sqlachemy query
    into a list of dictionaries, with column headings used as keys, but potentially general
    purpose for any data structured this way."""
    return [{k: v for k, v in zip(headings, row)} for row in rows]
    

def get_table_data(tablename: str, database: Session):
    table = get_table(tablename, database)
    rows = database.query(table).all()
    headings =  [d.get("name") for d in database.query(table).column_descriptions]
    return make_list_of_dicts(headings, rows)


DATABASE_URL = "postgresql+psycopg2://alan.maydwell@localhost/swamp"
#DATABASE_URL = "postgresql://alan.maydwell@localhost/feeschemes"

engine = sqlalchemy.create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
