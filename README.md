# Viktor Store Backend

A Django + Django REST Framework backend assignment that models an online store selling **books**, **music albums**, and **software licenses**.  
It includes a shopping cart system with total price/weight calculation.
---

## 🚀 Tech Stack
- **Python 3.11+**
- **Django 5.x**
- **Django REST Framework**
- **PostgreSQL**

---

## 🧩 Features
- Separate models for:
  - Book
  - MusicAlbum
  - SoftwareLicense
- Shopping cart to:
  - Add / remove products
  - Clear items
  - Compute total price and total weight
- Django admin for manual management
- REST API endpoints for CRUD and cart operations

---
## ⚙️ Setup

### Installation

1. **Clone the repository**
```bash
git clone <repo-url>
cd viktor_store_assessment
```

2. **Install dependencies using Poetry**
```bash
poetry install
```

3. **Activate the Poetry virtual environment**
```bash
poetry shell
```

4. **Set up environment variables**
Create a `.env` file in the project root with the following variables:
```env
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=viktor_store
DB_USERNAME=postgres
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=5432
PAGE_SIZE=10
```

5. **Create PostgreSQL database**
```bash
createdb viktor_store
```

6. **Run migrations**
```bash
python manage.py migrate
```

7. **Create a superuser (optional, for Django admin)**
```bash
python manage.py createsuperuser
```

8. **Run the development server**
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

---

## 📚 API Endpoints

### Base URL
All API endpoints are prefixed with `/v1/api/`

### Products

#### Books
- `GET /v1/api/books/` - List all books
- `GET /v1/api/books/{id}/` - Retrieve a book
- `POST /v1/api/books/` - Create a book
- `PUT /v1/api/books/{id}/` - Update a book
- `PATCH /v1/api/books/{id}/` - Partially update a book
- `DELETE /v1/api/books/{id}/` - Delete a book

**Book Fields:**
- `id` (UUID)
- `title` (string)
- `author` (string)
- `number_of_pages` (integer)
- `price` (decimal, EUR)
- `weight` (decimal, kg)
- `created_at` (datetime)
- `updated_at` (datetime)

#### Music Albums
- `GET /v1/api/albums/` - List all albums
- `GET /v1/api/albums/{id}/` - Retrieve an album
- `POST /v1/api/albums/` - Create an album
- `PUT /v1/api/albums/{id}/` - Update an album
- `PATCH /v1/api/albums/{id}/` - Partially update an album
- `DELETE /v1/api/albums/{id}/` - Delete an album

**Album Fields:**
- `id` (UUID)
- `artist` (string)
- `title` (string)
- `number_of_tracks` (integer)
- `price` (decimal, EUR)
- `weight` (decimal, kg)
- `created_at` (datetime)
- `updated_at` (datetime)

#### Software Licenses
- `GET /v1/api/licenses/` - List all licenses
- `GET /v1/api/licenses/{id}/` - Retrieve a license
- `POST /v1/api/licenses/` - Create a license
- `PUT /v1/api/licenses/{id}/` - Update a license
- `PATCH /v1/api/licenses/{id}/` - Partially update a license
- `DELETE /v1/api/licenses/{id}/` - Delete a license

**License Fields:**
- `id` (UUID)
- `name` (string)
- `price` (decimal, EUR)
- `weight` (decimal, kg - should be 0 or null)
- `created_at` (datetime)
- `updated_at` (datetime)

### Shopping Cart

#### Cart Operations
- `GET /v1/api/carts/` - List all carts
- `GET /v1/api/carts/{id}/` - Retrieve a cart (includes total_price and total_weight)
- `POST /v1/api/carts/` - Create a new cart
- `DELETE /v1/api/carts/{id}/` - Delete a cart

#### Add Item to Cart
- `POST /v1/api/carts/{id}/add-item/`

**Request Body:**
```json
{
  "model": "book|musicalbum|softwarelicense",
  "id": "<product-uuid>",
  "quantity": 1
}
```

#### Remove Item from Cart
- `POST /v1/api/carts/{id}/remove-item/`

**Request Body:**
```json
{
  "model": "book|musicalbum|softwarelicense",
  "id": "<product-uuid>",
  "quantity": 1
}
```

#### Clear Cart
- `POST /v1/api/carts/{id}/clear/`

**Response includes:**
- `total_price` - Total price of all items in EUR
- `total_weight` - Total weight of all items in kg

---

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

---


