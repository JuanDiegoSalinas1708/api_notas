import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# Base de datos temporal en memoria
notas_db: Dict[int, dict] = {}
contador_id = 1

# Modelo de Nota
class Nota(BaseModel):
    titulo: str
    contenido: str

# -----------------------------
#        ENDPOINTS
# -----------------------------

# GET - Endpoint principal
@app.get("/")
def home():
    return {"message": "API de notas funcionando correctamente 🚀"}

# GET - Obtener todas las notas
@app.get("/notas")
def obtener_notas():
    return notas_db

# POST - Crear una nueva nota
@app.post("/notas", status_code=201)
def crear_nota(nota: Nota):
    global contador_id
    notas_db[contador_id] = {"id": contador_id, **nota.dict()}
    contador_id += 1
    return {"mensaje": "Nota creada", "nota": notas_db[contador_id - 1]}

# PUT - Actualizar una nota por ID
@app.put("/notas/{id_nota}")
def actualizar_nota(id_nota: int, nota: Nota):
    if id_nota not in notas_db:
        raise HTTPException(status_code=404, detail="Nota no encontrada")

    notas_db[id_nota].update(nota.dict())
    return {"mensaje": "Nota actualizada", "nota": notas_db[id_nota]}

# DELETE - Borrar una nota por ID
@app.delete("/notas/{id_nota}")
def eliminar_nota(id_nota: int):
    if id_nota not in notas_db:
        raise HTTPException(status_code=404, detail="Nota no encontrada")

    nota_eliminada = notas_db.pop(id_nota)
    return {"mensaje": "Nota eliminada", "nota": nota_eliminada}

# -----------------------------
#     SERVIDOR PARA RENDER
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

