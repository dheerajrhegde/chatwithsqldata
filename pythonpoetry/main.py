from fastapi import FastAPI
import uvicorn
from pythonpoetry.com.github.dheerajhegde.api import build_pipeline

"""def include_router(app):
    app.include_router(router.router)

def start_application():
    app = FastAPI()
    include_router(app)
    return app

if __name__ == "__main__":
    app = start_application()
    uvicorn.run(app)"""

app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/chat")
async def chat(query: str):
    response, df = build_pipeline.run_full_pipeline(query)
    return {"response": response, "df": df.to_dict()}

if __name__ == "__main__":
    uvicorn.run(app)