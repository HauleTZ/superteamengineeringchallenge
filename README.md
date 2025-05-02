# Superteam Engineering Challenge – Payment Plan API 💸

## 🚀 Overview

This project is a RESTful API for managing **payment plans** where users can save weekly toward purchasing products. When a user’s total contributions reach the product's price, a **simulated payout** is triggered and logged.

Built with Django and Django Rest Framework, this solution includes unit tests, logging, and Swagger documentation for easy exploration.

---

## 🛠 Features

- Create payment plans linked to specific products
- Make weekly contributions (e.g. TZS 5,000/week)
- Track progress toward the target amount
- Automatically mark plans as completed and simulate payout
- Swagger/OpenAPI documentation
- Unit tests for core logic

---

## 📦 Tech Stack

- Python 3.13.2
- Django 5.2
- Django REST Framework
- drf-yasg (Swagger)
- SQLite (default)

---

## 🔧 Setup Instructions

1. **Clone the project:**
   ```bash
   git clone https://github.com/<your-username>/superteamengineeringchallenge.git
   cd superteamengineeringchallenge

2. **Create virtual environment & install dependencies:**

python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

3. **Run migrations:**

python manage.py migrate

4. **Run server:**

python manage.py runserver

5. **Access Swagger docs:**

    http://127.0.0.1:8000/swagger/




🔍 Example Usage

    Create a user → Create a payment plan → Contribute weekly → Reach goal → Simulated payout is logged.

Sample log:

[PAYOUT] Simulated payout for user 'testuser' on plan ID 1 - Product: Smartphone, Amount: 20000 TZS

🧪 Tests

Run all tests:

python manage.py test payments




 Design Decisions

    Django ORM was chosen to model relational data cleanly and maintain referential integrity between users, products, and payment plans.

    Django REST Framework (DRF) viewsets and serializers were used to ensure clean separation of concerns, enhance code reusability, and accelerate development.

    Contributions are recorded as individual entries to provide a complete transaction history and enable future auditability.

    total_saved is implemented as a computed property rather than a stored field to ensure real-time accuracy and avoid data redundancy.

    Payout simulation is handled using Django’s logging framework to keep the process safe and transparent during development and testing.

    API documentation is auto-generated with drf-yasg (Swagger) for easy exploration and integration by third parties or front-end teams.
