from pydantic import BaseModel, EmailStr, Field, PositiveFloat, PositiveInt


class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=4)


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class OrderItemIn(BaseModel):
    sku: str = Field(min_length=1)
    name: str = Field(min_length=1)
    unit_price: PositiveFloat
    qty: PositiveInt


class OrderCreate(BaseModel):
    items: list[OrderItemIn] = Field(min_length=1)


class OrderItemOut(BaseModel):
    sku: str
    name: str
    unit_price: float
    qty: int


class OrderOut(BaseModel):
    id: int
    items: list[OrderItemOut]
