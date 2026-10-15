from decimal import Decimal
from pydantic import BaseModel, ConfigDict
class ProductOut(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int; sku:str; name:str; slug:str; category:str; description:str|None; price:Decimal; prep_minutes:int|None; featured:bool
