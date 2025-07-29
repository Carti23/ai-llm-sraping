import numpy as np

from app.scraper import analyze_comments, generate_embeddings, parse_product_html


def test_parse_product_html():
    html_content = "<html><h1>Test Product</h1><img src='http://example.com/image.jpg'><p class='comment'>Great product!</p></html>"
    title, images, comments = parse_product_html(html_content)
    assert title == "Test Product"
    assert images == ['http://example.com/image.jpg']
    assert comments == ['Great product!']


def test_analyze_comments():
    comments = ['Great product!']
    sentiments = analyze_comments(comments)
    assert sentiments['Great product!'] in ['positive', 'neutral', 'negative']


def test_generate_embeddings():
    comments = ['Great product!']
    vectors = generate_embeddings(comments)
    assert isinstance(vectors, np.ndarray)
    assert vectors.shape[0] == 1 