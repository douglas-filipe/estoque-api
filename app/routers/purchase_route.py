from fastapi import APIRouter, Depends, HTTPException, WebSocketDisconnect, WebSocket
from sqlalchemy.orm import Session
from app.crud import purchase_crud, product_crud
from app.schemas import purchase_schema
from app.database.db import get_db
from typing import List

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    print('websocket', websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if data['event'] == 'purchase_made':
                print(f"Purchase made: {data['data']}")
                await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.post("/purchase", response_model=purchase_schema.Purchase)
def post_purchase(purchase: purchase_schema.PurchaseCreate, db: Session = Depends(get_db)):
    find_product = product_crud.get_product_by_id(db=db, product_id=purchase.product_id)
    validate_quantity = product_crud.get_product_quantity(db=db, product_id=purchase.product_id, quantity=purchase.quantity)
    
    if(purchase.quantity==0):
        raise HTTPException(status_code=400, detail="Valor inválido") 
    
    if(find_product is None):
       raise HTTPException(status_code=404, detail="Produto não encontrado") 
   
    if(validate_quantity is None):
       raise HTTPException(status_code=400, detail="Quantidade não disponível!")  
   
    product_crud.update_product_quantity(db=db,product_id=purchase.product_id, quantity=purchase.quantity)

    create_purchase = purchase_crud.create_purchase(db=db, purchase=purchase)
    
    return create_purchase

@router.get("/purchase", response_model=list[purchase_schema.Purchase])
def get_purchases(db: Session = Depends(get_db)):
    purchases = purchase_crud.get_purchases(db)
    return purchases

@router.get("/purchase/last", response_model=list[purchase_schema.Purchase])
def get_last_purchases(db: Session = Depends(get_db)):
    purchases = purchase_crud.get_last_purchases(db)
    return purchases

@router.get("/purchase/top", response_model=list[purchase_schema.TopSellingProduct])
def get_top_selling_products(db: Session = Depends(get_db)):
    purchases = purchase_crud.get_top_selling_products(db)
    return purchases