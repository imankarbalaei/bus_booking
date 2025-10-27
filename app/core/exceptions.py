# from fastapi import status
# from typing import Optional
#
#
# class BaseAppException(Exception):
#     """کلاس پایه برای تمام خطاهای اختصاصی سیستم رزرو اتوبوس"""
#
#     def __init__(self, detail: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
#         self.detail = detail
#         self.status_code = status_code
#         super().__init__(self.detail)
#
#
# class AuthException(BaseAppException):
#     """خطاهای مربوط به احراز هویت (مثلاً نام کاربری/رمز عبور اشتباه، توکن نامعتبر)"""
#
#     def __init__(self, detail: str, status_code: int = status.HTTP_401_UNAUTHORIZED):
#         super().__init__(detail, status_code)
#
#
# class NotFoundException(BaseAppException):
#     """خطا در صورت پیدا نشدن موجودیت (مثلاً کاربر، سفر، اتوبوس)"""
#
#     def __init__(self, detail: str, status_code: int = status.HTTP_404_NOT_FOUND):
#         super().__init__(detail, status_code)
#
#
# class ConflictException(BaseAppException):
#     """خطا در صورت تداخل یا نقض محدودیت (مثلاً شماره موبایل تکراری، صندلی رزرو شده)"""
#
#     def __init__(self, detail: str, status_code: int = status.HTTP_409_CONFLICT):
#         super().__init__(detail, status_code)
#
# # ... می‌توان خطاهای دیگری مانند BookingException و AdminException را اضافه کرد