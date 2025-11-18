from fastapi import APIRouter, Depends, HTTPException
from app.db import get_conn
from app.models import CouponCreate
from app.services.coupon_logic import validate_coupon_details
import json

router = APIRouter()

@router.post("/coupons")
def create_coupon(data: CouponCreate):
    # 1. Validate the "details" based on the type
    validate_coupon_details(data.type, data.details)

    # 2. Insert into DB using raw SQL
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO coupons (type, details) VALUES (?, ?)",
        (data.type, json.dumps(data.details))
    )
    conn.commit()

    coupon_id = cursor.lastrowid

    # 3. Return created coupon
    return {
        "id": coupon_id,
        "type": data.type,
        "details": data.details
    }
