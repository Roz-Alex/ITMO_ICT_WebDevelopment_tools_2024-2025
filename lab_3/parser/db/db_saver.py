from db.connection import get_session
from db.models import User, Gender


async def save_user_async(user_data: dict):
    async for session in get_session():
        async with session.begin():
            user = User(
                name=user_data["name"],
                email=user_data["email"],
                pass_hash=user_data["pass_hash"],
                age=user_data.get("age"),
                country=user_data.get("country"),
                gender=Gender(user_data["gender"]) if user_data.get("gender") else None,
            )
            session.add(user)
        await session.refresh(user)
