from .db import DataBase

async def expiration_manager():
    async with DataBase() as db:
        rowcount = await db.delete_after_time()
    return rowcount
    