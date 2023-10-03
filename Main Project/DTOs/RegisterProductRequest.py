from pydantic import BaseModel
class RegisterProductRequest(BaseModel):
    product_name:str 
    description : str
    price :int
    quantity_in_stock:int
    transaction_type:str
    admin_id:int