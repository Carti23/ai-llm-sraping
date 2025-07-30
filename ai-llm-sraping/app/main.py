import os
import asyncio
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


class ProductHTML(BaseModel):
    html_content: str = Field(
        ...,
        example=open('app/data/sample_product.html').read() if os.path.exists('app/data/sample_product.html') else "<html>...</html>"
    )


@app.get("/product/{product_id}")
async def get_product(product_id: int):
    def fetch_product_and_comments():
        session: Session = SessionLocal()
        try:
            product = session.query(Product).filter(Product.id == product_id).first()
            if not product:
                return None, []
            comments = session.query(Comment).filter(Comment.product_id == product_id).all()
            return product, comments
        finally:
            session.close()

    product, comments = await asyncio.to_thread(fetch_product_and_comments)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "title": product.title,
        "image_urls": product.image_urls.split(','),
        "comments": [c.text for c in comments],
        "sentiments": {c.text: c.sentiment for c in comments}
    }


@app.post("/product/", summary="Create a product from HTML content")
async def create_product(data: ProductHTML):
    product_id, images = await asyncio.to_thread(process_product, data.html_content, True)

    await asyncio.gather(*(upload_image_to_gcs(image_url) for image_url in images))

    return {"id": product_id, "message": "Product created successfully"}
