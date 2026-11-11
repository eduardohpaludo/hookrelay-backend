import uuid
from datetime import datetime
from fastapi import APIRouter, FastAPI, Request, status, HTTPException
import base64

app = FastAPI()

router = APIRouter()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/health")
def health():
    return {"status": "ok"}


bins: dict[str, list[dict]] = {}

@app.post("/api/bins", status_code=201)
def create_bin(request: Request) -> dict:
    bin_id = uuid.uuid4().hex
    bins[bin_id] = []

    return {"bin_id": bin_id, "url": str(request.base_url) + f"h/{bin_id}"}

@app.get("/api/bins/{bin_id}/requests")
def list_bin(bin_id: str):
    if bin_id not in bins:
            raise HTTPException(status_code=404, detail="Bin not found")
    return bins[bin_id][::-1]

@app.api_route("/h/{bin_id}", methods=[
    "GET", "POST", "DELETE", "OPTIONS", "PUT", "QUERY", "PATCH"
])
async def catch_all(request: Request, bin_id: str):
    if bin_id not in bins:
        raise HTTPException(status_code=404, detail="Bin not found")

    raw = await request.body()

    content = base64.b64encode(raw).decode("utf-8")
    
    bins[bin_id].append(
        {
            "method": request.method, 
            "body" : content,
            "headers": dict(request.headers),
            "date": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
    )
    return {}