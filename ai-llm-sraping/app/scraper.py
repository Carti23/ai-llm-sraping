import faiss
import numpy as np
import openai
from bs4 import BeautifulSoup

from .database import SessionLocal
from .faiss_index import add_vectors_to_faiss
from .models import Comment, Product
from .sentiment import analyze_sentiment


def parse_product_html(html_content: str):
    soup = BeautifulSoup(html_content, 'lxml')
    title = soup.find('h1').text.strip()
    images = [img['src'] for img in soup.find_all('img')]
    comments = [comment.text.strip() for comment in soup.find_all('p', class_='comment')]
    return title, images, comments

def analyze_comments(comments: list[str]) -> dict:
    return {comment: analyze_sentiment(comment) for comment in comments}

def generate_embeddings(comments: list[str]) -> np.ndarray:
    vectors = []
    for comment in comments:
        emb = openai.Embedding.create(model="text-embedding-ada-002", input=comment)
        vectors.append(np.array(emb['data'][0]['embedding'], dtype='float32'))
    return np.array(vectors)

def save_product_with_comments(title: str, images: list[str], comments: list[str], sentiments: dict) -> int:
    session = SessionLocal()
    try:
        new_product = Product(
            title=title,
            image_urls=','.join(images),
            comments=','.join(comments),
            sentiments=','.join([f'{c}: {s}' for c, s in sentiments.items()])
        )
        session.add(new_product)
        session.commit()
        session.refresh(new_product)

        for text, sentiment in sentiments.items():
            comment = Comment(
                product_id=new_product.id,
                text=text,
                sentiment=sentiment
            )
            session.add(comment)
        session.commit()

        return new_product.id
    finally:
        session.close()

def process_product(html_content: str, return_images: bool = False):
    title, images, comments = parse_product_html(html_content)
    sentiments = analyze_comments(comments)
    vectors = generate_embeddings(comments)
    product_id = save_product_with_comments(title, images, comments, sentiments)
    add_vectors_to_faiss(vectors, product_id)

    if return_images:
        return product_id, images
    return product_id, None

