# Інтернет-магазин вінілових платівок

## Опис проєкту
Сайт для купівлі та перегляду вінілових платівок. Сервіс дозволяє шукати релізи за назвою альбому, фільтрувати платівки за виконавцями та жанрами, переглядати детальний трекліст і наявність на складі, а також оформлювати замовлення зі збереженням історії покупок.

### Основні можливості 
- **Клієнт:**
  * Перегляд повного каталогу платівок із пагінацією, сортуванням та фільтрами.
  * Сторінки виконавців та жанрів із переліком їхніх релізів.
  * Детальна сторінка платівки з інформацією про ціну, рік випуску, обкладинку, кількість на складі та список треків.
  * Оформлення замовлення (списує 1 шт. зі складу та фіксує покупку).
  * Реєстрація та вхід за допомогою email і пароля.
- **Адміністратор:**
  * Додавання нових платівок, виконавців і жанрів.
  * Редагування інформації та видалення позицій.

---

## Архітектура REST API

### 1. Платівки (`/records`)

### `GET /records`
- **Query-параметри:**
  * `search` (string) — пошук за назвою альбому.
  * `artist_id` (integer) — фільтрація за ID виконавця.
  * `genre_id` (integer) — фільтрація за ID жанру.
  * `sort` (string) — поле сортування. Доступні значення:
    * `price` — за зростанням ціни (asc)
    * `-price` — за спаданням ціни (desc)
    * `year` — за роком випуску (asc)
    * `-year` — за роком випуску від найновіших (desc)
  * `page` (integer), `limit` (integer) — параметри пагінації.
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

### `GET /records/{id}`
- **Response Status:** `200 OK`
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

### `POST /records`
- **Response Status:** `201 Created`
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

### `PUT /records/{id}`
- **Response Status:** `200 OK`
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

### `DELETE /records/{id}`
- **Response Status:** `204 No Content`

---

### 2. Виконавці (`/artists`)

### `GET /artists`
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

### `POST /artists`
- **Response Status:** `201 Created`
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

---

### 3. Жанри (`/genres`)

### `GET /genres`
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

### `POST /genres`
- **Response Status:** `201 Created`
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

---

### Фрагмент 2. Оновлена секція `4. Замовлення (/orders)`

```markdown
### 4. Замовлення (`/orders`)

### `POST /orders`
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

### `GET /orders`
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

### `POST /auth/register`
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

### `POST /auth/login`
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



## Схема бази даних

![Схема бази даних](<./Untitled Diagram.drawio.png>)
