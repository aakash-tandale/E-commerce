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


@router.get("/Coupons")
def get_all_coupons():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT id, type, details FROM coupons")
    rows = cursor.fetchall()

    coupons = []
    for row in rows:
        coupon_id, coupon_type, details_json = row
        coupons.append({
            "id": coupon_id,
            "type": coupon_type,
            "details": json.loads(details_json)
        })

    return {"coupons": coupons}


@router.get("/coupons/{coupon_id}")
def get_coupon_by_id(coupon_id: int):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT id, type, details FROM coupons WHERE id = ?", (coupon_id,))
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Coupon not found")

    coupon_id, coupon_type, details_json = row

    return {
        "id": coupon_id,
        "type": coupon_type,
        "details": json.loads(details_json)
    }


@router.delete("/coupons/{coupon_id}")
def delete_coupon(coupon_id: int):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM coupons WHERE id = ?", (coupon_id,))
    exists = cursor.fetchone()

    if not exists:
        raise HTTPException(status_code=404, detail="Coupon not found")

    cursor.execute("DELETE FROM coupons WHERE id = ?", (coupon_id,))
    conn.commit()

    return {"message": "Coupon deleted successfully", "coupon_id": coupon_id}



@router.put("/coupons/{coupon_id}")
def update_coupon(coupon_id: int, data: CouponCreate):
    conn = get_conn()
    cursor = conn.cursor()

    # 1. Ensure coupon exists
    cursor.execute("SELECT id FROM coupons WHERE id = ?", (coupon_id,))
    existing = cursor.fetchone()
    if not existing:
        raise HTTPException(status_code=404, detail="Coupon not found")

    # 2. Strict validation of updated details
    validate_coupon_details(data.type, data.details)

    # 3. Update using raw SQL
    try:
        cursor.execute(
            "UPDATE coupons SET type = ?, details = ? WHERE id = ?",
            (data.type, json.dumps(data.details), coupon_id)
        )
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # 4. Return updated coupon
    return {
        "id": coupon_id,
        "type": data.type,
        "details": data.details
    }
