# 🛒 Product Scraper API (FastAPI + LLM + FAISS + GCS)

This project implements an API for:
- Parsing a product HTML page (title, images, comments).
- Sentiment analysis of comments using **OpenAI GPT-3.5**.
- Storing results in **PostgreSQL**.
- Creating vector embeddings of comments in **FAISS**.
- Uploading images to **Google Cloud Storage**.
- Containerization via **Docker**.

---

## ⚙️ Environment Variables (ENV)

Create a `.env` file in the root and specify:

```env
DATABASE_URL=...
OPENAI_API_KEY=...
GOOGLE_APPLICATION_CREDENTIALS=...
GCS_BUCKET_NAME=...
```

## 🚀 Running the Project with Docker Compose

1️⃣ Build the containers:

```bash
docker-compose build
```

2️⃣ Start the containers:

```bash
docker-compose up
```

3️⃣ Access the API:

Open Swagger UI:
👉 http://localhost:8000/docs

## 🧪 Running Tests

Execute inside the container:

```bash
docker-compose exec app sh -c 'PYTHONPATH=/app pytest tests --maxfail=1 --disable-warnings -v'
```

## 🔍 Request Examples

▶️ POST /product/

Request body:

```json
{
  "html_content": "<html>\n<head><title>Smart Fitness Watch</title></head>\n<body>\n    <h1>Smart Fitness Watch</h1>\n    <img src=\"https://example.com/images/watch-front.jpg\" alt=\"Front view\">\n    <img src=\"https://example.com/images/watch-back.jpg\" alt=\"Back view\">\n    <img src=\"https://example.com/images/watch-box.jpg\" alt=\"Box\">\n    <div class=\"reviews\">\n        <div class=\"review\"><p class=\"comment\">I love this watch! It tracks my workouts perfectly.</p></div>\n        <div class=\"review\"><p class=\"comment\">Battery life is okay, but it could be better.</p></div>\n        <div class=\"review\"><p class=\"comment\">Terrible experience, it stopped working after a week.</p></div>\n        <div class=\"review\"><p class=\"comment\">Good value for the price. Syncs easily with my phone.</p></div>\n    </div>\n</body>\n</html>"
}
```

Response:

```json
{
  "id": 1,
  "message": "Product created successfully"
}
```

▶️ GET /product/{id}

Example response:

```json
{
  "title": "Smart Fitness Watch",
  "image_urls": [
    "https://example.com/images/watch-front.jpg",
    "https://example.com/images/watch-back.jpg",
    "https://example.com/images/watch-box.jpg"
  ],
  "comments": [
    "I love this watch! It tracks my workouts perfectly.",
    "Battery life is okay, but it could be better.",
    "Terrible experience, it stopped working after a week.",
    "Good value for the price. Syncs easily with my phone."
  ],
  "sentiments": [
    "I love this watch! It tracks my workouts perfectly.: positive",
    "Battery life is okay, but it could be better.: neutral",
    "Terrible experience, it stopped working after a week.: negative",
    "Good value for the price. Syncs easily with my phone.: positive"
  ]
}
```

## 🛑 Stopping the Containers

```bash
docker-compose down
```

## 📂 Technology Stack

- FastAPI – API and Swagger documentation
- BeautifulSoup (bs4) – HTML parsing
- OpenAI GPT-3.5 – Sentiment analysis of comments
- PostgreSQL + SQLAlchemy – Database
- FAISS – Vector search for embeddings
- Google Cloud Storage – Image storage
- Docker + docker-compose – Containerization
- isort – Import sorting

## 📜 License

MIT License

## 🤔 Why These Choices?

- **FAISS vs. Pinecone:** FAISS обрано, бо це швидкий і безкоштовний інструмент для роботи з векторним пошуком. Він легко налаштовується і підходить для локального використання. Pinecone більше підходить для хмарних сервісів, але FAISS достатній і дешевший для цього проєкту.

- **PostgreSQL ORM — SQLAlchemy:** PostgreSQL обрано за його надійність, масштабованість та розширену підтримку складних типів даних і індексації. Він добре підходить для обробки складних запитів і великих наборів даних, що робить його ідеальним вибором для застосунків, які потребують надійного та ефективного зберігання даних. SQLAlchemy дозволяє легко взаємодіяти з PostgreSQL через ORM, спрощуючи створення та управління моделями без необхідності писати складні SQL-запити вручну.

- **OpenAI:** OpenAI обрано за його передові можливості обробки природної мови, які є важливими для точного аналізу тональності коментарів. Модель здатна розуміти та генерувати текст, схожий на людський, що робить її цінним інструментом для покращення користувацького досвіду в застосунках, які потребують розуміння мови.