from pydantic import BaseModel
class InventoryUpdateRequest(BaseModel):
   product_id:int 
   quantity_changed:int  
   transaction_type:str 
   adminId:int

