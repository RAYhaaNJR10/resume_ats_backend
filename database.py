from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
import os

password = quote_plus(os.getenv("MYSQLPASSWORD"))

DATABASE_URL = (
    f"mysql+pymysql://"
    f"{os.getenv('MYSQLUSER')}:"
    f"{password}@"
    f"{os.getenv('MYSQLHOST')}:"
    f"{os.getenv('MYSQLPORT')}/"
    f"{os.getenv('MYSQLDATABASE')}"
)

engine = create_engine(DATABASE_URL)

print("MySQL connection created")

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)