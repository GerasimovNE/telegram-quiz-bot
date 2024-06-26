import aiosqlite
import os
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.getenv('DB_NAME')

async def create_table_result():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_results (user_id INTEGER PRIMARY KEY, user_name VARCHAR, result INTEGER)''')
        await db.commit()
            
async def update_result(user_id,user_name,result):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_results (user_id, user_name, result) VALUES (?, ?, ?)', (user_id,user_name, result))
        await db.commit()

async def get_users_result():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT * FROM quiz_results ORDER BY result ASC') as users_results:
            return await users_results.fetchall()

async def get_result(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT result FROM quiz_state WHERE user_id = (?)',(user_id,)) as result:
            user_result = await result.fetchone()
            if user_result[0] is None:
                return 0
            else:
                return user_result[0]

async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER, result INTEGER)''')
        await db.commit()

async def update_quiz_state(user_id, question_index, result):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index, result) VALUES (?, ?, ?)', (user_id, question_index,result))
        await db.commit()

async def get_question_index(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)',(user_id,)) as cursore:
            question_index = await cursore.fetchone()
            if question_index[0] is not None:
                return question_index[0]
            else:
                return 0
            
