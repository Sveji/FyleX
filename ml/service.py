from fastapi import FastAPI
from pydantic import BaseModel
from utt import extract_text_from_url
from predict.predict import prediction
from transformers import pipeline

summarizer = pipeline("summarization", model="Falconsai/text_summarization")

class AnalysisModel(BaseModel):
    url: str

app = FastAPI()

@app.post("/api/service/analysis")
def analysis(item: AnalysisModel):
    text = extract_text_from_url(url=item.url)
    pred = prediction(text)
    return pred

@app.post("/api/service/summary")
def summary(item: AnalysisModel):
    text = extract_text_from_url(url=item.url)
    summary = summarizer(text, max_length=10000, min_length=30, do_sample=False)[0]
    return summary
    
