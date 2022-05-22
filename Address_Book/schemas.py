from pydantic import BaseModel


class Address(BaseModel):
    latitude: float
    longitude: float
    name: str
    address: str
    phone_no: int
    pincode: int
    email: str
