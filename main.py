from fastapi import FastAPI

app = FastAPI()

from auth_routes import auth_router
from webhook_routes import webhook_router

app.include_router(auth_router)
app.include_router(webhook_router)

# Pra rodar o projeto, executar no terminal o comando: uvicorn main:app --reload