from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from DB.ORM.Config import DATABASE_URL
from contextlib import contextmanager
from DB.ORM.Base import Base
from LoggerConfig import pulse_database_logger as logger

@contextmanager
def session_scope():
    engine = create_engine(DATABASE_URL)
    logger.info("Connected to database")
    session = scoped_session(sessionmaker(bind=engine))
    logger.info("Session created successfully")
    Base.metadata.create_all(engine)
    logger.info("All Tables created successfully")
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(e)
    finally:
        session.remove()
