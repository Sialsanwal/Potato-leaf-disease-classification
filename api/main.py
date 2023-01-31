import numpy as np
from fastapi import FastAPI, UploadFile,File
import uvicorn
from io import BytesIO
from PIL import Image

app= FastAPI()

@app.get("/ping")
async def ping():
    return "Hello World"
def read_file_as_image(data) ->np.ndarray:
    image= np.array(Image.open(BytesIO(data)))
    return image
@app.post("/predict")
async def predict(
        file: UploadFile = File(...)

):
    bytes= read_file_as_image(await file.read())
    pass
if __name__=="__main__":
    uvicorn.run(app,host='localhost',port=8000)