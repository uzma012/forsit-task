from pydantic import BaseModel
class InventoryResponse(BaseModel):
   product_id:int 
   product_name:str  
   quantity:int 
   status:str

