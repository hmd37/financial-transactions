from fastapi import FastAPI

from .routers import transactions, users

app = FastAPI()

app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(transactions.router, prefix="/api", tags=["Transactions"])
