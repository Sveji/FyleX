from fastapi import FastAPI
from pydantic import BaseModel
from utt import extract_text_from_url
from predict.predict import prediction
from llm.llm import process_review
from qa.qa import answer_question
from transformers import pipeline

summarizer = pipeline("summarization", model="Falconsai/text_summarization")



class AnalysisModel(BaseModel):
    url: str

class ReviewModel(BaseModel):
    url: str
    analysis: list

class QAModel(BaseModel):
    url: str
    question: str

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

@app.post("/api/service/review")
def review(item: ReviewModel):
    analysis = item.analysis
    url = item.url
    text = extract_text_from_url(url=url)
    contact = f"Text: {text} Suspicious sentences: {analysis}"
    reviews = process_review(contact)
    return reviews


@app.post("/api/service/qa")
def qa(item: QAModel):
    context = extract_text_from_url(url=item.url)
    question = item.question
    answer = answer_question(question, context)
    return {
        "answer": answer
    }
