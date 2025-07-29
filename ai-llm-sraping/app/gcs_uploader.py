import os

from google.cloud import storage

GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "test-bucket-roman")

storage_client = storage.Client()

def upload_image_to_gcs(image_url: str, bucket_name: str = GCS_BUCKET_NAME):
    bucket = storage_client.bucket(bucket_name)
    file_name = image_url.split("/")[-1]

    blob = bucket.blob(file_name)
    blob.upload_from_string(f"Dummy image data from {image_url}", content_type="image/jpeg")
