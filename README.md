# پروژه با Docker و Alembic

این پروژه با استفاده از Docker و Docker Compose اجرا می‌شود و شامل مدیریت دیتابیس با Alembic و بارگذاری داده‌های اولیه است.

## پیش‌نیازها
- Docker نصب شده
- Docker Compose نصب شده

## راه‌اندازی پروژه

1. **ساخت و اجرای کانتینرها**

```bash
docker compose up -d --build

2. **migration**

docker compose exec web alembic upgrade head

3. **seed Data**

docker compose exec web python -m app.db.seed


اطلاعات کاربری

برای ورود به API:

کاربر: admin

شماره تماس: 09121112211

پسورد: 12345678

توقف پروژه

برای متوقف کردن کانتینرها:

docker compose down