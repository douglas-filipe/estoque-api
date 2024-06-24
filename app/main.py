from fastapi import FastAPI
from app.database.db import engine, Base
from app.routers import user_route, auth_route, category_route, product_route, purchase_route
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(user_route.router)
app.include_router(auth_route.router, prefix="/auth")
app.include_router(category_route.router)
app.include_router(product_route.router)
app.include_router(purchase_route.router)