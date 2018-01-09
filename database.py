from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# engine = create_engine('sqlite:////tmp/catalog.db', convert_unicode=True)
engine = create_engine('postgresql://grader:great4321@localhost:5432/catalog')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # do we need to import this?
    import test
    Base.metadata.create_all(bind=engine)