from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field
class OrderItemCreate(BaseModel): product_id:int; quantity:int=Field(gt=0,le=100)
class OrderCreate(BaseModel): branch_id:int; delivery_type:str=Field(pattern="^(RECOLECCION|DOMICILIO)$"); shipping_cost:Decimal=Decimal("0"); items:list[OrderItemCreate]
class OrderItemOut(BaseModel): product_id:int; name:str; quantity:int; unit_price:Decimal; subtotal:Decimal
class OrderOut(BaseModel): id:int; number:str; status:str; created_at:datetime; total:Decimal; items:list[OrderItemOut]=[]
