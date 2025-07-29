import os

from fastapi import FastAPI, HTTPException
from google.cloud import storage
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine
from .gcs_uploader import upload_image_to_gcs
from .models import Comment, Product
from .scraper import process_product

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Product API",
)

GCS_CREDENTIALS = "/app/keys/key.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GCS_CREDENTIALS



class ProductHTML(BaseModel):
    html_content: str = Field(
        ...,
        example=open('app/data/sample_product.html').read() if os.path.exists('app/data/sample_product.html') else "<html>...</html>"
    )

@app.get("/product/{product_id}")
def get_product(product_id: int):
    session: Session = SessionLocal()
    product = session.query(Product).filter(Product.id == product_id).first()
    if not product:
        session.close()
        raise HTTPException(status_code=404, detail="Product not found")

    comments = session.query(Comment).filter(Comment.product_id == product_id).all()
    session.close()

    return {
        "title": product.title,
        "image_urls": product.image_urls.split(','),
        "comments": [c.text for c in comments],
        "sentiments": {c.text: c.sentiment for c in comments}
    }

@app.post("/product/", summary="Create a product from HTML content")
def create_product(data: ProductHTML):
    product_id, images = process_product(data.html_content, return_images=True)

    for image_url in images:
        upload_image_to_gcs(image_url)

    return {"id": product_id, "message": "Product created successfully"}
