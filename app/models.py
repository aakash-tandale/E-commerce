from pydantic import BaseModel, Field
from typing import List

# ----- Cart-wise -----
class CartWiseDetails(BaseModel):
    threshold: float
    discount: float  # percentage


# ----- Product-wise -----
class ProductWiseDetails(BaseModel):
    product_id: int
    discount: float  # percentage


# ----- BxGy -----
class BxGyProduct(BaseModel):
    product_id: int
    quantity: int


class BxGyDetails(BaseModel):
    buy_products: List[BxGyProduct]
    get_products: List[BxGyProduct]
    repetition_limit: int = Field(..., alias="repition_limit")  


# ----- Main Coupon Create Model -----
class CouponCreate(BaseModel):
    type: str
    details: dict
