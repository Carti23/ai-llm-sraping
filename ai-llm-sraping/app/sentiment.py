import os

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_sentiment(comment):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Classify the sentiment as: positive, neutral, or negative."},
            {"role": "user", "content": comment}
        ]
    )
    return response.choices[0].message['content'].strip().lower()
