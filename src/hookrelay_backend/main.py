import uuid

from fastapi import FastAPI, Request

app = FastAPI()


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
