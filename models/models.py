from pydantic import BaseModel, EmailStr, SecretStr, Field
from typing import Optional

class User(BaseModel):
    Email: EmailStr
    Username: str
    Name: str
    Password: SecretStr

class Address(BaseModel):
    location: str
    district: Optional[str]
    pincode: Optional[str] = Field(max_length=6, min_length=6)

class Supplier(BaseModel):
    name: str
    phone: Optional[str] = Field(min_length=10, max_length=10)
    gstin: Optional[str] = Field(title="GSTIN", description="GSTIN of the supplier", min_length=15, max_length=15)
    address: Address

class Category(BaseModel):
    category: str