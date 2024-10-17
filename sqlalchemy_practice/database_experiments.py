import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
# Imports below only used in type hints
from sqlalchemy.sql.schema import Table


#DATABASE_URL = "postgresql://alan.maydwell@localhost/feeschemes"
DATABASE_URL = "postgresql+psycopg2://alan.maydwell@localhost/swamp"

class Database:
    def __init__(self, url):
        self.url = url
        self.engine = db.create_engine(url)
        self.meta_data = db.MetaData()
        self.meta_data.reflect(bind=self.engine)
        
    def get_table(self, table_name: str) -> Table | None:
        return self.meta_data.tables.get(table_name, None)
    


def get_metadata(db):
    engine = db.get_bind()
    meta_data = db.MetaData()
    return meta_data.reflect(bind=engine)
    
    

if __name__ == "__main__":
    print("Start **************************")
    """
    mydb = Database(DATABASE_URL)
    feeschemes_table = mydb.get_table("feeschemes")
    # Does not get rows, just makes SQL
    sql = feeschemes_table.select()
    print(sql)
    
    with mydb.engine.connect() as dbconn:
        quasi_cursor = dbconn.execute(sql)
        results =  quasi_cursor.fetchall()
        print(results)
        
        """


    engine = db.create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    #print(dir(session))
    
    meta_data = db.MetaData()
    meta_data.reflect(bind=engine)
    table_name = "creatures" #"feeschemes"
    table = meta_data.tables.get(table_name)
    
    results = session.query(table).all()
    descriptions = session.query(table).column_descriptions
    column_names = [d.get("name") for d in descriptions]

    for row in results: 
        print(row)
        
    print(column_names)
    print(">>>>")
    print(dir(session))
