from fastapi import HTTPException
from app.models import (
    CartWiseDetails,
    ProductWiseDetails,
    BxGyDetails
)

def validate_coupon_details(coupon_type: str, details: dict):
    """
    Validates the coupon 'details' field based on the type.
    Raises HTTPException(400) on validation error.
    """
    try:
        if coupon_type == "cart-wise":
            CartWiseDetails(**details)
        elif coupon_type == "product-wise":
            ProductWiseDetails(**details)
        elif coupon_type == "bxgy":
            BxGyDetails(**details)
        else:
            raise HTTPException(status_code=400, detail="Invalid coupon type")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid details structure: {str(e)}")
