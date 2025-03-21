from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_KEY = os.getenv("GROQ_KEY") 

client = Groq(
    api_key=GROQ_KEY
)

def process_review(input_text):
    prompt = (
    "Analyze each suspicious sentence from the provided text and give a brief explanation for why it is suspicious. "
    "Output exactly as a comma-separated list of JSON objects, each on one line, with keys exactly "
    '"suspicious text" and "explanation". Do not include any extra text, newlines, or internal reasoning. '
    "Only output the final JSON objects in the required format. "
    "Example: {\"suspicious text\": \"We are pleased to inform you that your account has been pre-approved for an exclusive \", \"explanation\": \"Creates false exclusivity.\"} "
    "Now process this input:\n" + input_text
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    return chat_completion.choices[0].message.content