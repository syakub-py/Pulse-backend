from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from DB.ORM.Config import DATABASE_URL
from contextlib import contextmanager
from DB.ORM.Base import Base

@contextmanager
def session_scope():
    engine = create_engine(DATABASE_URL)
    session = scoped_session(sessionmaker(bind=engine))
    Base.metadata.create_all(engine)
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.remove()
