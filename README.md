# Personalized Product Recommendation API

This project is a Flask-based API that provides personalized product recommendations using a modular architecture inspired by the Model-Context-Protocol (MCP) pattern.

## 📦 Features
- Personalized recommendations based on user affinity (brands, categories)
- Context-aware filtering using user metadata (location, income)
- Rule-based fallback for guest users
- JSON API with Swagger documentation
- Pydantic validation for request schema

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/prashant11gupta/ranker.git
cd ranker
```

### 2. Set up the environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the server
```bash
export FLASK_APP=app.py 
export FLASK_ENV=development
python app.py
```

### 4. Access the API
- Swagger Docs: [http://localhost:5000/apidocs](http://localhost:5000/apidocs)
- Endpoint: `POST /recommend`

---

## 📤 Example Request
```json
{
  "top_n": 4,
  "user": {
    "location": "CA",
    "user_id": 3
  }
}
```

## 📥 Example Response
```json
{
  "data": {
    "recommended_products": [
      {
        "brand": "Samsung",
        "category": "Electronics",
        "id": 103,
        "name": "Galaxy S21",
        "price": 799
      },
      {
        "brand": "Apple",
        "category": "Electronics",
        "id": 101,
        "name": "iPhone",
        "price": 999
      },
      ...
    ]
  }
}
```

---
## 🧱 Project Structure
```
.
├── app.py                # Flask entrypoint
├── agent.py              # Main agent class
├── model.py              # Product ranking and recommendation logic
├── context.py            # Context resolver from request
├── protocol.py           # Request/response contract
├── db/
│   ├── product_catalog.py
│   └── user_affinities.py
|   └── user.py
├── schemas.py            # Pydantic validation schemas
├── requirements.txt
└── README.md
```
