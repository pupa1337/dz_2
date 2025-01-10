from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Shoe(BaseModel):
    id: int
    brand: str
    model: str
    size: float
    color: str
    price: float

shoes: List[Shoe] = []

@app.post("/shoes/", response_model=Shoe)
def create_shoe(shoe: Shoe):
    if any(s.id == shoe.id for s in shoes):
        raise HTTPException(status_code=400, detail="Такая обувь уже есть")
    shoes.append(shoe)
    return shoe

@app.get("/shoes/", response_model=List[Shoe])
def read_shoes():
    return shoes

@app.get("/shoes/{shoe_id}", response_model=Shoe)
def read_shoe(shoe_id: int):
    shoe = next((s for s in shoes if s.id == shoe_id), None)
    if shoe is None:
        raise HTTPException(status_code=404, detail=f"Обувь {shoe_id} не найдена")
    return shoe

@app.put("/shoes/{shoe_id}", response_model=Shoe)
def update_shoe(shoe_id: int, updated_shoe: Shoe):
    index = next((i for i, s in enumerate(shoes) if s.id == shoe_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail=f"Обувь {shoe_id} не найдена")
    if updated_shoe.id != shoe_id:
        raise HTTPException(status_code=400, detail="Ошибка")
    shoes[index] = updated_shoe
    return updated_shoe

@app.delete("/shoes/{shoe_id}", response_model=Shoe)
def delete_shoe(shoe_id: int):
    index = next((i for i, s in enumerate(shoes) if s.id == shoe_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail=f"Обувь {shoe_id} не найдена")
    return shoes.pop(index)
