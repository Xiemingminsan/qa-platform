from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine, text
import os

DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE_URL:", DATABASE_URL)

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar()
        print("DB Connected! Result:", result)
except Exception as e:
    print("DB ERROR:", e)

