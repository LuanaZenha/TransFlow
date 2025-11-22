import os
from typing import List
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.models.corrida_model import Corrida
from src.database.mongo_client import get_collection
from src.database.redis_client import get_saldo
from src.producer import broker, publish_corrida_finalizada


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await broker.start()


@app.on_event("shutdown")
async def shutdown():
    await broker.close()


@app.post("/corridas")
async def criar_corrida(corrida: Corrida):
    payload = corrida.model_dump()
    await publish_corrida_finalizada(payload)
    return JSONResponse({"status": "publicado", "id_corrida": corrida.id_corrida})


@app.get("/corridas", response_model=List[dict])
async def listar_corridas():
    coll = get_collection()
    itens = []
    async for d in coll.find({}, {"_id": 0}):
        itens.append(d)
    return itens


@app.get("/corridas/{forma_pagamento}", response_model=List[dict])
async def listar_por_pagamento(forma_pagamento: str):
    coll = get_collection()
    itens = []
    async for d in coll.find({"forma_pagamento": forma_pagamento}, {"_id": 0}):
        itens.append(d)
    return itens


@app.get("/saldo/{motorista}")
async def saldo_motorista(motorista: str):
    saldo = await get_saldo(motorista)
    return {"motorista": motorista, "saldo": saldo}


@app.get("/saldos")
async def listar_saldos():
    coll = get_collection()
    nomes = await coll.distinct("motorista.nome")
    resultados = []
    for nome in nomes:
        s = await get_saldo(nome)
        resultados.append({"motorista": nome, "saldo": s})
    return resultados


app.mount("/ui", StaticFiles(directory="src/static", html=True), name="ui")


@app.get("/config")
async def get_config():
    return {"googleMapsApiKey": os.getenv("GOOGLE_MAPS_API_KEY", "")}
