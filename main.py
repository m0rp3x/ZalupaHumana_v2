from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = FastAPI()

engine = create_engine('mysql://koval:P@ssw0rd@localhost:3306/koval')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"

    ID = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    Contact_Info = Column(String)

class Equipment(Base):
    __tablename__ = "equipment"

    ID = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    Serial_Number = Column(String)
    Client_ID = Column(Integer, ForeignKey("clients.ID"))

class Request(Base):
    __tablename__ = "requests"

    ID = Column(Integer, primary_key=True, index=True)
    Registration_Date = Column(Date)
    Equipment_ID = Column(Integer, ForeignKey("equipment.ID"))
    Status = Column(String)
    Progress = Column(String)

class ClientCreate(BaseModel):
    Name: str
    Contact_Info: str


class ClientResponse(BaseModel):
    ID: int
    Name: str
    Contact_Info: str


class ClientUpdate(BaseModel):
    ID: int
    Name: str
    Contact_Info: str

class EquipmentCreate(BaseModel):
    Name: str
    Serial_Number: str
    Client_ID: int

class EquipmentUpdate(BaseModel):
    ID: int
    Name: str
    Serial_Number: str
    Client_ID: int

class EquipmentSchema(BaseModel):
    ID: int
    Name: str
    Serial_Number: str
    Client_ID: int

    class Config:
        orm_mode = True

class RequestCreate(BaseModel):
    Registration_Date: str
    Equipment_ID: int
    Status: str
    Progress: str

class RequestUpdate(BaseModel):
    ID: int
    Registration_Date: str
    Equipment_ID: int
    Status: str
    Progress: str

class RequestModel(BaseModel):
    ID: int
    Registration_Date: str
    Equipment_ID: int
    Status: str
    Progress: str

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/clients/", response_model=ClientResponse)
def create_client(client: ClientCreate):
    db = next(get_db())
    new_client = Client(**client.dict())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

@app.get("/clients/", response_model=List[ClientResponse])
def read_clients():
    db = next(get_db())
    clients = db.query(Client).all()
    return clients

@app.get("/clients/{client_id}", response_model=ClientResponse)
def read_client(client_id: int):
    db = next(get_db())
    client = db.query(Client).filter(Client.ID == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@app.put("/clients/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, client: ClientUpdate):
    db = next(get_db())
    updated_client = db.query(Client).filter(Client.ID == client_id).first()
    if updated_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    for key, value in client.dict().items():
        setattr(updated_client, key, value)
    db.commit()
    db.refresh(updated_client)
    return updated_client

@app.delete("/clients/{client_id}")
def delete_client(client_id: int):
    db = next(get_db())
    client = db.query(Client).filter(Client.ID == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()
    return {"detail": "Client deleted"}

# Оборудование
@app.post("/equipment/", response_model=EquipmentSchema)
def create_equipment(equipment: EquipmentCreate):
    db = next(get_db())
    new_equipment = Equipment(**equipment.dict())
    db.add(new_equipment)
    db.commit()
    db.refresh(new_equipment)
    return new_equipment

@app.get("/equipment/", response_model=List[EquipmentSchema])
def read_equipment():
    db = next(get_db())
    equipment = db.query(Equipment).all()
    return equipment

@app.get("/equipment/{equipment_id}", response_model=EquipmentSchema)
def read_equipment_by_id(equipment_id: int):
    db = next(get_db())
    equipment = db.query(Equipment).filter(Equipment.ID == equipment_id).first()
    if equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment

@app.put("/equipment/{equipment_id}", response_model=EquipmentSchema)
def update_equipment(equipment_id: int, equipment: EquipmentUpdate):
    db = next(get_db())
    updated_equipment = db.query(Equipment).filter(Equipment.ID == equipment_id).first()
    if updated_equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    for key, value in equipment.dict().items():
        setattr(updated_equipment, key, value)
    db.commit()
    db.refresh(updated_equipment)
    return updated_equipment

@app.delete("/equipment/{equipment_id}")
def delete_equipment(equipment_id: int):
    db = next(get_db())
    equipment = db.query(Equipment).filter(Equipment.ID == equipment_id).first()
    if equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    db.delete(equipment)
    db.commit()
    return {"detail": "Equipment deleted"}

# Заявки
@app.post("/requests/", response_model=RequestModel)
def create_request(request: RequestCreate):
    db = next(get_db())
    new_request = Request(**request.dict())
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

@app.get("/requests/", response_model=List[RequestModel])
def read_requests():
    db = next(get_db())
    requests = db.query(Request).all()
    return requests

@app.get("/requests/{request_id}", response_model=RequestModel)
def read_request_by_id(request_id: int):
    db = next(get_db())
    request = db.query(Request).filter(Request.ID == request_id).first()
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return request

@app.put("/requests/{request_id}", response_model=RequestModel)
def update_request(request_id: int, request: RequestUpdate):
    db = next(get_db())
    updated_request = db.query(Request).filter(Request.ID == request_id).first()
    if updated_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    for key, value in request.dict().items():
        setattr(updated_request, key, value)
    db.commit()
    db.refresh(updated_request)
    return updated_request

@app.delete("/requests/{request_id}")
def delete_request(request_id: int):
    db = next(get_db())
    request = db.query(Request).filter(Request.ID == request_id).first()
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    db.delete(request)
    db.commit()
    return {"detail": "Request deleted"}
