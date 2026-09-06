from sqlalchemy.orm import sessionmaker
from app.db.engine import engine

sessionlocal = sessionmaker(bind=engine)