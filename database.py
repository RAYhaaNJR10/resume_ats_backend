from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os
from sqlalchemy.orm import sessionmaker

load_dotenv()

password = quote_plus(os.getenv("DB_PASSWORD"))

DATABASE_URL = (
    f"mysql+pymysql://"
    f"{os.getenv('DB_USER')}:"
    f"{password}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)

print("MySQL connection created")

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)