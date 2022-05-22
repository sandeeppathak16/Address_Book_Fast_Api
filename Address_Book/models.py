from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float

from database import Base


class Address_Book(Base):
    __tablename__ = "Address_Book"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, unique=True, index=True)
    longitude = Column(Float, unique=True, index=True)
    name = Column(String, index=True)
    address = Column(String, index=True)
    phone_no = Column(Integer, index=True)
    pincode = Column(Integer, index=True)
    email = Column(String, index=True)