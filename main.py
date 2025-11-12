import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Property, Savedsearch, Lead

app = FastAPI(title="Proplift Next - Real Estate Investing API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Real Estate Investing API is running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "❌ Not Set",
        "database_name": "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    return response

# Simple deal feed endpoints
@app.get("/api/properties", response_model=List[Property])
def list_properties(limit: int = 12, city: Optional[str] = None, state: Optional[str] = None):
    filt = {}
    if city:
        filt["city"] = city
    if state:
        filt["state"] = state
    try:
        docs = get_documents("property", filter_dict=filt, limit=limit)
        # convert ObjectId and unknown fields
        cleaned = []
        for d in docs:
            d.pop("_id", None)
            cleaned.append(Property(**d))
        return cleaned
    except Exception as e:
        # If DB not available, return empty list rather than 500 to keep UI working in demo
        return []

@app.post("/api/properties")
def create_property(item: Property):
    try:
        inserted_id = create_document("property", item)
        return {"id": inserted_id, "status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/savedsearches")
def create_saved_search(s: Savedsearch):
    try:
        inserted_id = create_document("savedsearch", s)
        return {"id": inserted_id, "status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/leads")
def create_lead(lead: Lead):
    try:
        inserted_id = create_document("lead", lead)
        return {"id": inserted_id, "status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
