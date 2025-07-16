from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Behavior

DB_USER = "postgres"
DB_PASSWORD = "admin123"  # cambia por tu clave real
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "sensores_db"

DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/sensores_db"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        if db.query(Behavior).count() == 0:
            db.add_all([
                Behavior(name="sawtooth"),
                Behavior(name="square"),
                Behavior(name="triangle"),
            ])
            db.commit()

