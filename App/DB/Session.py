from typing import Generator
from sqlalchemy import create_engine
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, scoped_session, Session

from App.DB.Base import Base
from App.DB.Config import DATABASE_URL
from LoggerConfig import pulse_database_logger as logger

@contextmanager
def session_scope() -> Generator[scoped_session[Session], None, None]:
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
