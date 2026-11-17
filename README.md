# rest_vinyl_shop — Інтернет-магазин вінілових платівок (Backend API)

## Опис проєкту

Серверна частина (REST API) для купівлі та перегляду вінілових платівок. Сервіс дозволяє шукати релізи за назвою альбому, фільтрувати платівки за виконавцями та жанрами, переглядати детальний трекліст і наявність на складі, а також керувати каталогом (CRUD для платівок, виконавців та жанрів).

### Основні можливості

- **Клієнт:**
  - Перегляд повного каталогу платівок із пагінацією, сортуванням та фільтрами.
  - Перегляд виконавців та жанрів.
  - Детальна інформація про платівку: ціна, рік випуску, обкладинка, кількість на складі та список треків.
- **Адміністратор:**
  - Створення, редагування та видалення платівок, виконавців і жанрів.
  - Захист цілісності даних: заборона видалення виконавця або жанру, за якими закріплені платівки (`409 Conflict`).

---

## Як запустити проєкт

1. **Клонуйте репозиторій та перейдіть у папку проєкту:**

   ```bash
   git clone <посилання_на_репозиторій>
   cd rest_vinyl_shop
   ```

2. **Створіть та активуйте віртуальне середовище:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Встановіть залежності:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Виконайте міграції:**

   ```bash
   python manage.py migrate
   ```

5. **Запустіть сервер:**

   ```bash
   python manage.py runserver
   ```

Бекенд буде доступний за адресою: [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## Обробка помилок

Усі ендпоінти повертають помилки в єдиному JSON-форматі:

```json
{
  "error": "Опис причини помилки або словник помилок валідації"
}
```

- `400 Bad Request` — невалідні вхідні дані (наприклад, від'ємна ціна, некоректний рік випуску, порожні обов'язкові поля або неіснуючий `artist_id`).
- `404 Not Found` — звернення до об'єкта за ID, якого не існує.
- `409 Conflict` — спроба видалити виконавця або жанр, за якими закріплені платівки в каталозі.

---

## Архітектура REST API

### 1. Платівки (`/records`)

#### GET /records

- **Query-параметри:**
  - `search` (string) — пошук за назвою альбому.
  - `artist_id` (integer) — фільтрація за ID виконавця.
  - `genre_id` (integer) — фільтрація за ID жанру.
  - `sort` (string) — поле сортування. Доступні значення:
    - `price` — за зростанням ціни (asc)
    - `-price` — за спаданням ціни (desc)
    - `year` — за роком випуску (asc)
    - `-year` — за роком випуску від найновіших (desc)
  - `page` (integer), `limit` (integer) — параметри пагінації.
- **Response Status:** `200 OK`
- **Response Body:**

```json
[
  {
    "id": 1,
    "album": "",
    "artist": "",
    "genre": "",
    "price": 0.0,
    "year": 0,
    "cover_image": ""
  }
]
```

#### GET /records/{id}

- **Response Status:** `200 OK` (або `404 Not Found`)
- **Response Body:**

```json
{
  "id": 1,
  "album": "",
  "artist_id": 0,
  "artist": "",
  "genre_id": 0,
  "genre": "",
  "price": 0.0,
  "year": 0,
  "cover_image": "",
  "stock_quantity": 0,
  "tracklist": [
    "",
    ""
  ]
}
```

#### POST /records

- **Response Status:** `201 Created` (або `400 Bad Request`)
- **Request Body:**

```json
{
  "album": "",
  "artist_id": 0,
  "genre_id": 0,
  "price": 0.0,
  "year": 0,
  "cover_image": "",
  "stock_quantity": 0,
  "tracklist": [
    "",
    ""
  ]
}
```

- **Response Body:**

```json
{
  "id": 1,
  "album": "",
  "artist_id": 0,
  "artist": "",
  "genre_id": 0,
  "genre": "",
  "price": 0.0,
  "year": 0,
  "cover_image": "",
  "stock_quantity": 0,
  "tracklist": [
    "",
    ""
  ]
}
```

#### PUT /records/{id}

- **Response Status:** `200 OK` (або `400 Bad Request`, `404 Not Found`)
- **Request Body:**

```json
{
  "album": "",
  "artist_id": 0,
  "genre_id": 0,
  "price": 0.0,
  "year": 0,
  "cover_image": "",
  "stock_quantity": 0,
  "tracklist": [
    "",
    ""
  ]
}
```

- **Response Body:**

```json
{
  "id": 1,
  "album": "",
  "artist_id": 0,
  "artist": "",
  "genre_id": 0,
  "genre": "",
  "price": 0.0,
  "year": 0,
  "cover_image": "",
  "stock_quantity": 0,
  "tracklist": [
    "",
    ""
  ]
}
```

#### DELETE /records/{id}

- **Response Status:** `204 No Content` (або `404 Not Found`)

---

### 2. Виконавці (`/artists`)

#### GET /artists

- **Response Status:** `200 OK`
- **Response Body:**

```json
[
  {
    "id": 0,
    "name": "",
    "bio": "",
    "image_url": ""
  }
]
```

#### GET /artists/{id}

- **Response Status:** `200 OK` (або `404 Not Found`)
- **Response Body:**

```json
{
  "id": 0,
  "name": "",
  "bio": "",
  "image_url": ""
}
```

#### POST /artists

- **Response Status:** `201 Created` (або `400 Bad Request`)
- **Request Body:**

```json
{
  "name": "",
  "bio": "",
  "image_url": ""
}
```

- **Response Body:**

```json
{
  "id": 0,
  "name": "",
  "bio": "",
  "image_url": ""
}
```

#### PUT /artists/{id}

- **Response Status:** `200 OK` (або `400 Bad Request`, `404 Not Found`)
- **Request Body:**

```json
{
  "name": "",
  "bio": "",
  "image_url": ""
}
```

- **Response Body:**

```json
{
  "id": 0,
  "name": "",
  "bio": "",
  "image_url": ""
}
```

#### DELETE /artists/{id}

- **Response Status:** `204 No Content` (або `404 Not Found`, `409 Conflict` якщо за виконавцем закріплені платівки)

---

### 3. Жанри (`/genres`)

#### GET /genres

- **Response Status:** `200 OK`
- **Response Body:**

```json
[
  {
    "id": 0,
    "name": ""
  }
]
```

#### GET /genres/{id}

- **Response Status:** `200 OK` (або `404 Not Found`)
- **Response Body:**

```json
{
  "id": 0,
  "name": ""
}
```

#### POST /genres

- **Response Status:** `201 Created` (або `400 Bad Request`)
- **Request Body:**

```json
{
  "name": ""
}
```

- **Response Body:**

```json
{
  "id": 0,
  "name": ""
}
```

#### PUT /genres/{id}

- **Response Status:** `200 OK` (або `400 Bad Request`, `404 Not Found`)
- **Request Body:**

```json
{
  "name": ""
}
```

- **Response Body:**

```json
{
  "id": 0,
  "name": ""
}
```

#### DELETE /genres/{id}

- **Response Status:** `204 No Content` (або `404 Not Found`, `409 Conflict` якщо до жанру прив'язані платівки)

---

### 4. Замовлення (`/orders`)

> **TODO:** Детальна реалізація замовлень буде на наступних етапах.

#### POST /orders

- **Response Status:** `201 Created`
- **Request Body:**

```json
{
  "items": [
    {
      "record_id": 0,
      "quantity": 0
    },
    {
      "record_id": 0,
      "quantity": 0
    }
  ]
}
```

- **Response Body:**

```json
{
  "order_id": 0,
  "status": "",
  "total_price": 0.0,
  "created_at": "",
  "items": [
    {
      "record_id": 0,
      "album": "",
      "quantity": 0,
      "price_per_item": 0.0
    },
    {
      "record_id": 0,
      "album": "",
      "quantity": 0,
      "price_per_item": 0.0
    }
  ]
}
```

#### GET /orders

- **Response Status:** `200 OK`
- **Response Body:**

```json
[
  {
    "order_id": 0,
    "status": "",
    "total_price": 0.0,
    "created_at": "",
    "items": [
      {
        "record_id": 0,
        "album": "",
        "quantity": 0,
        "price_per_item": 0.0
      },
      {
        "record_id": 0,
        "album": "",
        "quantity": 0,
        "price_per_item": 0.0
      }
    ]
  }
]
```

---

### 5. Аутентифікація (`/auth`)

> **TODO:** Детальна реалізація auth буде на наступних етапах.

#### POST /auth/register

- **Response Status:** `201 Created`
- **Request Body:**

```json
{
  "email": "",
  "password": ""
}
```

- **Response Body:**

```json
{
  "id": 0,
  "email": ""
}
```

#### POST /auth/login

- **Response Status:** `200 OK`
- **Request Body:**

```json
{
  "email": "",
  "password": ""
}
```

- **Response Body:**

```json
{
  "message": "Вхід успішний"
}
```

---

## Схема бази даних

![Схема бази даних](docs/db_schema.png)

## Authentication & Authorization (JWT)

Проєкт використовує **JWT (JSON Web Token)** автентифікацію на базі `djangorestframework-simplejwt`.

### Передача токена (Headers)

Для доступу до захищених ендпоінтів необхідно передавати `access` токен у HTTP-заголовку:

```http
Authorization: Bearer <access_token>
```

- Час життя `access` токена: **15 хвилин**
- Час життя `refresh` токена: **7 днів**

---

## Ендпоінти автентифікації

### 1. Реєстрація користувача

- **URL:** `/auth/register`
- **Метод:** `POST`
- **Доступ:** Public
- **Headers:** `Content-Type: application/json`

**Request Body:**

```json
{
  "username": "vinyl_lover",
  "first_name": "Taras",
  "last_name": "Shevchenko",
  "email": "taras@example.com",
  "password": "StrongPass123!",
  "password_confirmation": "StrongPass123!"
}
```

**Обов'язкові поля:**

- `username` — до 150 символів, унікальний
- `email` — коректний формат, до 254 символів, унікальний
- `password` — 8–128 символів, перевірка складності
- `password_confirmation` — має збігатися з `password`

**Необов'язкові поля:** `first_name`, `last_name` (до 150 символів).

**Response (201 Created):**

```json
{
  "id": 2,
  "username": "vinyl_lover",
  "first_name": "Taras",
  "last_name": "Shevchenko",
  "email": "taras@example.com",
  "is_staff": false,
  "role": "user"
}
```

**Response (400 Bad Request — помилка валідації):**

```json
{
  "error": {
    "email": ["Введіть коректну email-адресу."],
    "password_confirmation": ["Паролі не збігаються."]
  }
}
```

---

### 2. Логін (отримання JWT токенів)

- **URL:** `/auth/login`
- **Метод:** `POST`
- **Доступ:** Public
- **Headers:** `Content-Type: application/json`

**Request Body:**

```json
{
  "username": "vinyl_lover",
  "password": "StrongPass123!"
}
```

**Response (200 OK):**

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (401 Unauthorized — невірний логін або пароль):**

```json
{
  "detail": "No active account found with the given credentials"
}
```

---

### 3. Оновлення Access токена

- **URL:** `/auth/refresh`
- **Метод:** `POST`
- **Доступ:** Public
- **Headers:** `Content-Type: application/json`

**Request Body:**

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (401 Unauthorized — невалідний або прострочений refresh токен):**

```json
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

---

### 4. Профіль поточного користувача

- **URL:** `/auth/me`
- **Метод:** `GET`
- **Доступ:** Authenticated
- **Headers:** `Authorization: Bearer <access_token>`

**Response (200 OK):**

```json
{
  "id": 2,
  "username": "vinyl_lover",
  "first_name": "Taras",
  "last_name": "Shevchenko",
  "email": "taras@example.com",
  "is_staff": false,
  "role": "user"
}
```

---

## Коди помилок доступу

### 401 Unauthorized

Запит до захищеного ендпоінта без заголовка `Authorization` або з простроченим/невалідним токеном:

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden

Спроба звичайного користувача (`is_staff: false`) виконати дію, доступну лише адміністратору (наприклад, `POST /artists` або `DELETE /genres/1`):

```json
{
  "detail": "Доступ заборонено. Ця дія дозволена лише адміністраторам."
}
```
