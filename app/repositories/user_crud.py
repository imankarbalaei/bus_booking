# from sqlalchemy import select
#
# from app.models import Wallet
# from app.models.user_model import User
# from app.db.database import async_session
#
# async def get_user_by_phone(phone_number: str):
#     async with async_session() as session:
#         result = await session.execute(select(User).where(User.phone_number == phone_number))
#         return result.scalar_one_or_none()
#
# async def create_user(full_name: str, phone_number: str, email: str, hashed_password: str):
#     async with async_session() as session:
#         async with session.begin():
#             user = User(
#                 full_name=full_name,
#                 phone_number=phone_number,
#                 email=email,
#                 hashed_password=hashed_password
#             )
#             session.add(user)
#             await session.flush()
#
#             wallet = Wallet(
#                 user_id=user.id,
#                 price=0
#             )
#             session.add(wallet)
#             return user
