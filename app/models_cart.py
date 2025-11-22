from pydantic import BaseModel
from typing import List

class CartItem(BaseModel):
    product_id: int
    quantity: int
    price: float

class Cart(BaseModel):
    items: List[CartItem]
