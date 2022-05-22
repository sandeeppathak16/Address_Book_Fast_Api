from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, SessionLocal
import distance

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/add_address', status_code=status.HTTP_201_CREATED)
def create_address(request: schemas.Address, db: Session = Depends(get_db)):
    new_address = models.Address_Book(latitude=request.latitude,
                                      longitude=request.longitude,
                                      name=request.name,
                                      phone_no=request.phone_no,
                                      address=request.address,
                                      pincode=request.pincode,
                                      email=request.email
                                      )
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address


@app.put("/address/update", status_code=status.HTTP_202_ACCEPTED)
def update_address(request: schemas.Address, lan: float = 0, lon: float = 0, db: Session = Depends(get_db)):
    address = db.query(models.Address_Book).filter(models.Address_Book.latitude == lan,
                                                   models.Address_Book.longitude == lon)
    if not address.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Address not found')
    address.update(request.dict())
    db.commit()
    return {'address updated'}


@app.get("/addresses", status_code=200)
def get_all_address(db: Session = Depends(get_db)):
    all_address = db.query(models.Address_Book).all()
    return all_address


@app.get("/address", status_code=200)
def get_address(lan: float = 0, lon: float = 0, db: Session = Depends(get_db)):
    address = db.query(models.Address_Book).filter(models.Address_Book.latitude == lan,
                                                   models.Address_Book.longitude == lon).first()
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There is no address with given latitude, '
                                                                          'longitude')
    return address


@app.get("/address/location", status_code=200)
def address_with_in_distance(lan: float = 0, lon: float = 0, limit: int = 0, db: Session = Depends(get_db)):
    all_address = db.query(models.Address_Book).all()
    res = []
    print(all_address)
    if all_address is not None:
        for ele in all_address:
            print(distance.distance(lan, lon, ele.latitude, ele.longitude))

            if distance.distance(lan, ele.latitude, lon, ele.longitude) <= limit:
                res.append(ele)
    return res


@app.delete("/address/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(lan: float = 0, lon: float = 0, db: Session = Depends(get_db)):
    address = db.query(models.Address_Book).filter(models.Address_Book.latitude == lan,
                                                   models.Address_Book.longitude == lon)
    if not address.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Address not found')
    address.delete(synchronize_session=False)
    db.commit()
    return {'address deleted'}
