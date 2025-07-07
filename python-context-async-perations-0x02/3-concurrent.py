# 3-concurrent.py

import asyncio
import aiosqlite

DATABASE_NAME = 'users.db'

# Ensure the database is set up with some sample data
async def setup_database():
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER NOT NULL
            )
        ''')
        await db.execute("INSERT OR IGNORE INTO users (id, name, email, age) VALUES (1, 'Alice', 'alice@example.com', 30)")
        await db.execute("INSERT OR IGNORE INTO users (id, name, email, age) VALUES (2, 'Bob', 'bob@example.com', 45)")
        await db.execute("INSERT OR IGNORE INTO users (id, name, email, age) VALUES (3, 'Charlie', 'charlie@example.com', 50)")
        await db.commit()

# Async function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect(DATABASE_NAME) as db:
        cursor = await db.execute("SELECT * FROM users")
        rows = await cursor.fetchall()
        print("All users:")
        for row in rows:
            print(row)

# Async function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect(DATABASE_NAME) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        rows = await cursor.fetchall()
        print("Users older than 40:")
        for row in rows:
            print(row)

# Run both queries concurrently
async def fetch_concurrently():
    await setup_database()
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# Entry point
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())

