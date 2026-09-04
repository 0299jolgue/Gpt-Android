import uvicorn
from fastapi import FastAPI
from .app.config import HOST, PORT
from .app.routes import router

app = FastAPI(title='Gpt-Android Test Harness')
app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(app, host=HOST, port=PORT)
