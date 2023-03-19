from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
from io import BytesIO
from PIL import Image
import pytesseract

class Source(BaseModel):
    source: str
    
app = FastAPI()

def getScore(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    ocr_result = pytesseract.image_to_string(img).lower()
    score = 0
    if "energ" in ocr_result:
        score += 0.5
    if "kwh/1000h" in ocr_result:
        score += 0.2
    if "abcdefg" in ocr_result:
        score += 0.3
    return score


@app.post("/IsEnergyLabel")
async def isEnergyLabel(source:Source) -> JSONResponse:
    try:
        score = getScore(source.source)
        if score is not None:
            return JSONResponse(content={"IsEnergyLabel": score >= 0.5})
        else:
            return JSONResponse(content={"error": f"Could not read image!"})
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid request body format or an error occurred.") from e
    
 