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
    
def calculate_cart_wise(cart, details):
    threshold = details["threshold"]
    discount_percent = details["discount"]

    total = sum(item["quantity"] * item["price"] for item in cart["items"])

    if total >= threshold:
        return total * (discount_percent / 100)

    return 0

def calculate_product_wise(cart, details):
    product_id = details["product_id"]
    discount_percent = details["discount"]

    discount = 0

    for item in cart["items"]:
        if item["product_id"] == product_id:
            discount += item["quantity"] * item["price"] * (discount_percent / 100)

    return discount


def calculate_bxgy(cart, details):
    buy_products = details["buy_products"]
    get_products = details["get_products"]
    repetition_limit = details["repition_limit"]

    # Convert cart to dictionary for fast lookup
    cart_map = {item["product_id"]: item for item in cart["items"]}

    # 1. Count how many times the BUY condition is satisfied
    max_repetitions = float("inf")

    for bp in buy_products:
        pid = bp["product_id"]
        required_qty = bp["quantity"]

        if pid not in cart_map:
            return 0  # Cannot satisfy buy condition

        cart_qty = cart_map[pid]["quantity"]
        reps = cart_qty // required_qty
        max_repetitions = min(max_repetitions, reps)

    # 2. Apply repetition limit
    times = min(max_repetitions, repetition_limit)

    # 3. Calculate discount for GET products
    discount = 0

    for gp in get_products:
        pid = gp["product_id"]
        free_qty = gp["quantity"] * times

        # need to check if price exists in cart (or we assume 0 if not present)
        if pid in cart_map:
            price = cart_map[pid]["price"]
            discount += free_qty * price

    return discount



def apply_cart_wise(cart, details):
    threshold = details["threshold"]
    discount_percent = details["discount"]

    total = sum(item["quantity"] * item["price"] for item in cart["items"])

    if total >= threshold:
        discount = total * (discount_percent / 100)
    else:
        discount = 0

    # Annotate each item (no item-level discount)
    updated_items = []
    for item in cart["items"]:
        updated_items.append({
            **item,
            "total_discount": 0
        })

    final_price = total - discount

    return updated_items, total, discount, final_price


def apply_bxgy(cart, details):
    buy_products = details["buy_products"]
    get_products = details["get_products"]
    repetition_limit = details["repition_limit"]

    cart_map = {item["product_id"]: dict(item) for item in cart["items"]}

    # ---- Calculate repetitions ----
    max_reps = float("inf")
    for bp in buy_products:
        pid = bp["product_id"]
        req_qty = bp["quantity"]

        if pid not in cart_map:
            return cart["items"], 0, 0, 0  # Not applicable

        reps = cart_map[pid]["quantity"] // req_qty
        max_reps = min(max_reps, reps)

    times = min(max_reps, repetition_limit)

    # ---- Add free products ----
    total_discount = 0

    for gp in get_products:
        pid = gp["product_id"]
        free_qty = gp["quantity"] * times

        # If the free product already in cart → increase its quantity
        if pid in cart_map:
            price = cart_map[pid]["price"]
            cart_map[pid]["quantity"] += free_qty
        else:
            # Add new free item (need price = 0? No → price should be market price)
            # But we don't know the price, so assume price=0 → discount stays correct
            price = 0
            cart_map[pid] = {"product_id": pid, "quantity": free_qty, "price": price}

        total_discount += free_qty * price

    # ---- Prepare updated items ----
    updated_items = []
    total = 0

    for item in cart_map.values():
        subtotal = item["quantity"] * item["price"]
        total += subtotal

        updated_items.append({
            **item,
            "total_discount": 0  # discount applies centrally
        })

    final_price = total - total_discount

    return updated_items, total, total_discount, final_price



def apply_product_wise(cart, details):
    pid = details["product_id"]
    discount_percent = details["discount"]

    total = 0
    total_discount = 0
    updated_items = []

    for item in cart["items"]:
        item_total = item["quantity"] * item["price"]
        total += item_total

        if item["product_id"] == pid:
            item_discount = item_total * (discount_percent / 100)
        else:
            item_discount = 0

        total_discount += item_discount

        updated_items.append({
            **item,
            "total_discount": item_discount
        })

    final_price = total - total_discount

    return updated_items, total, total_discount, final_price

