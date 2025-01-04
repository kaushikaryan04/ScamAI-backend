from fastapi import FastAPI , Depends
from core.config import settings
from core.dependencies import db
from fastapi.middleware.cors import CORSMiddleware
from models.models import ScammerModel
from fastapi.exceptions import HTTPException
from bson import ObjectId




app = FastAPI(
    title = settings.APP_NAME,
    debug = settings.DEBUG_MODE,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db_client():
    await db.connect_mongodb()

@app.on_event("shutdown")
async def shutdown_db_client():
    await db.close_mongodb()


# scammer_collection = db.db["scammers"]

@app.post("/scammers/")
async def create_scammer(scammer: ScammerModel):
    collection = db.db["scammers"]
    result = await collection.insert_one(scammer.dict(exclude_unset=True))
    if result.inserted_id:
        return {"id": str(result.inserted_id)}
    raise HTTPException(status_code=400, detail="Failed to create record")



@app.get("/scammers/{scammer_id}")
async def get_scammer(scammer_id: str):
    collection = db.db["scammers"]
    try :
        object_id = ObjectId(scammer_id)
    except Exception as e :
        raise HTTPException(status_code=400, detail= f"Invalid ID {e}")
    scammer = await collection.find_one({"_id": object_id})
    if not scammer:
        raise HTTPException(status_code=404, detail="Scammer not found")
    scammer["_id"] = str(scammer["_id"])
    return ScammerModel(**scammer)


@app.get("/health")
async def health_check():
    try:
        await db.db.command("ping")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}
