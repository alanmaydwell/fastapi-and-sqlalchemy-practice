import sqlalchemy as sa 
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy_utils import database_exists, create_database

class Base(DeclarativeBase):
    pass

class Creatures(Base):
    __tablename__ = "creatures"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)


def get_column_values(tablecolumn, session):
    rows = session.query(tablecolumn).all()
    return [r[0] for r in rows]

def add_creature(name, session, commit=True):
    creature = Creatures(name=name)
    res = session.add(creature)
    if commit:
        session.commit()
        
def remove_all_creatures(session):
    session.query(Creatures).delete()
    session.commit()
    
    
dburl = "postgresql+psycopg2://alan.maydwell@localhost/swamp"
engine = sa.create_engine(dburl)
# Examples that use sqlite don't include an explicit database creation step but seems necessary for postgres
if not database_exists(dburl):
    create_database(dburl)

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

#remove_all_creatures(session)
wanted_creatures = ["Gila Monster", "Natterjack Toad", "Hairy-nosed Wombat", "Slow Loris", "Smoky Bat", "Cheshire Cat", "Slithy Tove", "Moose", "Another Moose", "Probable Penguin"]
current_creatures = get_column_values(Creatures.name, session)
to_be_added = [c for c in wanted_creatures if c not in current_creatures]

print("To be added:", to_be_added)

for creature in to_be_added:
    print("Adding:", creature)
    add_creature(creature, session)
    
print(type(Session))
print(type(session))

print("End") 
