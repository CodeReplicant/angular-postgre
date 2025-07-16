from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List
import random
from database import SessionLocal, init_db
from models import Sensor, Behavior
from wave_eval import evaluate_wave

app = FastAPI()
init_db()

class SensorCreate(BaseModel):
    name: str
    behavior_id: int

class SensorOut(BaseModel):
    id: int
    name: str
    behavior_id: int


    class Config:
        orm_mode = True


@app.post("/sensors", response_model=SensorOut)
def create_sensor(sensor: SensorCreate):
    with SessionLocal() as db:
        behavior = db.query(Behavior).filter_by(id=sensor.behavior_id).first()
        if not behavior:
            raise HTTPException(status_code=400, detail="Invalid behavior ID")
        new_sensor = Sensor(name=sensor.name, behavior_id=sensor.behavior_id)
        db.add(new_sensor)
        db.commit()
        db.refresh(new_sensor)
        return new_sensor


@app.get("/sensors", response_model=List[SensorOut])
def read_sensors():
    with SessionLocal() as db:
        return db.query(Sensor).all()


@app.get("/sensors/{sensor_id}", response_model=SensorOut)
def read_sensor(sensor_id: int):
    with SessionLocal() as db:
        sensor = db.query(Sensor).filter_by(id=sensor_id).first()
        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor not found")
        return sensor


@app.put("/sensors/{sensor_id}", response_model=SensorOut)
def update_sensor(sensor_id: int, sensor_data: SensorCreate):
    with SessionLocal() as db:
        sensor = db.query(Sensor).filter_by(id=sensor_id).first()
        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor not found")
        sensor.name = sensor_data.name
        sensor.behavior_id = sensor_data.behavior_id
        db.commit()
        db.refresh(sensor)
        return sensor


@app.delete("/sensors/{sensor_id}")
def delete_sensor(sensor_id: int):
    with SessionLocal() as db:
        sensor = db.query(Sensor).filter_by(id=sensor_id).first()
        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor not found")
        db.delete(sensor)
        db.commit()
        return {"detail": "Sensor deleted"}


@app.get("/simulate")
def simulate(sensors: List[int] = Query(...)):
    if not sensors:
        raise HTTPException(status_code=400, detail="Debe proporcionar al menos un sensor.")

    results = []

    with SessionLocal() as db:
        for sensor_id in sensors:
            sensor = db.query(Sensor).filter_by(id=sensor_id).first()
            if not sensor:
                raise HTTPException(
                    status_code=404,
                    detail=f"Sensor con ID {sensor_id} no existe en la base de datos."
                )
            value_input = random.randint(1, 100)
            simulated_value = evaluate_wave(value_input, sensor.behavior.name) 

            results.append({
                "sensor_name": sensor.name,
                "behavior": sensor.behavior.name,
                "value": simulated_value
            })

    return results

