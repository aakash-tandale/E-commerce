from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.dialects.sqlite import JSON

DATABASE_URL = "sqlite:///file:memdb1?mode=memory&cache=shared&uri=true"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

metadata = MetaData()

coupons_table = Table(
    "coupons",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("type", String, nullable=False),     # cart-wise / product-wise / bxgy
    Column("details", JSON, nullable=False)     # will store coupon details
)

def init_db():
    metadata.create_all(engine)

def get_conn():
    """Returns a raw DB connection."""
    return engine.raw_connection()
