from fastapi import FastAPI
from pydantic import BaseModel
from utt import extract_text_from_url
from predict.predict import prediction

class AnalysisModel(BaseModel):
    url: str

app = FastAPI()

@app.post("/api/service/analysis")
def analysis(item: AnalysisModel):
    text = extract_text_from_url(url=item.url)
    pred = prediction(text)
    return pred