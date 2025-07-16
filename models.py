from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Behavior(Base):
    __tablename__ = "behaviors"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    sensors = relationship("Sensor", back_populates="behavior")

class Sensor(Base):
    __tablename__ = "sensors"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    behavior_id = Column(Integer, ForeignKey("behaviors.id"), nullable=False)
    behavior = relationship("Behavior", back_populates="sensors")
