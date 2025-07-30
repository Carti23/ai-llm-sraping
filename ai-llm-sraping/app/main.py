import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .database import async_engine, AsyncSessionLocal, Base
from .gcs_uploader import upload_image_to_gcs
from .models import Comment, Product
from .scraper import process_product

Base.metadata.create_all(bind=async_engine)

app = FastAPI(title="Product API")


class ProductHTML(BaseModel):
    html_content: str = Field(
        ...,
        example=open('app/data/sample_product.html').read() if os.path.exists('app/data/sample_product.html') else "<html>...</html>"
    )

@app.get("/product/{product_id}")
async def get_product(product_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        result_comments = await session.execute(select(Comment).where(Comment.product_id == product_id))
        comments = result_comments.scalars().all()

        return {
            "title": product.title,
            "image_urls": product.image_urls.split(','),
            "comments": [c.text for c in comments],
            "sentiments": {c.text: c.sentiment for c in comments}
        }


@app.post("/product/", summary="Create a product from HTML content")
async def create_product(data: ProductHTML):
    product_id, images = await process_product(data.html_content, return_images=True)

    for image_url in images:
        await upload_image_to_gcs(image_url)

    return {"id": product_id, "message": "Product created successfully"}

