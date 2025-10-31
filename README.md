# پروژه رزرو بلیط اوتوبوس

این پروژه با استفاده از Docker و Docker Compose اجرا می‌شود و شامل مدیریت دیتابیس با Alembic و بارگذاری داده‌های اولیه است.

## Prerequisites
- Python 3.11+
- PostgreSQL
- Docker 

## راه‌اندازی پروژه

## clone 

```bash
https://github.com/imankarbalaei/bus_booking.git
```
**ساخت و اجرای کانتینرها**

```bash
docker compose up -d --build

```
## migration


```bash
docker compose exec web alembic upgrade head
```
3. **seed Data**

```bash
docker compose exec web python -m app.db.seed
```

**اطلاعات کاربری**

- admin
- phone_number:09121112211
- password:09121112211



توقف پروژه

```bash
docker compose down
```