from app.db.base import Base
from app.db.engine import engine

from app.modules.users.models.user import User

def create_tables():
    Base.metadata.create_all(bind=engine)

    