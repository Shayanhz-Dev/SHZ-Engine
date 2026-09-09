from sqlalchemy.orm import sessionmaker
from app.db.engine import engine

sessionlocal = sessionmaker(bind=engine)

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()