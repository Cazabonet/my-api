import uvicorn
from fastapi import FastAPI
from database import engine, Base
from app.routers import empresa
from app.models.empresa import Empresa

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def check_api():
    return {"response": "Api Online!"}

app.include_router(empresa.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)