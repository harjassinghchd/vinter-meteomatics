from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud, models, schema
from database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()



@app.get("/parameters/", response_model=None)
def get_parameters(lat: float, lon: float, starttime: str, endtime: str, type_of_data: str = 'all', type_of_table: str = 'wide', db: Session = Depends(get_db)):
	if type_of_data not in schema.dataTypes:
		raise HTTPException(status_code=404, detail="Data type not found")
	else:
		return crud.get_parameters(db, lat=lat, lon=lon, starttime=starttime, endtime=endtime, type_of_data=type_of_data, type_of_table=type_of_table)
