
import numpy as np
from fastapi import FastAPI, UploadFile,File
import uvicorn
from io import BytesIO
from PIL import Image
import tensorflow as tf
from tensorflow.python.client import device_lib
device_lib.list_local_devices()

app = FastAPI()
MODEL = tf.keras.models.load_model("../saved_models/1")
CLASS_NAME = ["Early Blight", "Late Blight", "Healthy"]

@app.get("/ping")
async def ping():
    return "Hello I am Alive"

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.post("/predict")
async def predict(
        file: UploadFile = File(...)

):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image,0)
    predictions = MODEL.predict(img_batch)
    predicted_class= CLASS_NAME[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    print(predicted_class,confidence)
    return {
        "class":predicted_class,
        "confidence": float(confidence)
    }



if __name__== "__main__":
    uvicorn.run(app, host='localhost',port=8080)



