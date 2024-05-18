import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def get_user(tg_id: int):
    with Session() as session:
        try:
            result = session.execute(text("SELECT * FROM users WHERE tg_id = :tg_id"), {'tg_id': tg_id}).fetchone()
            if result:
                return dict(result)
            else:
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

def add_user(tg_id: int, tg_chat_id: int, tg_username: str, full_name: str):
    with Session() as session:
        try:
            session.execute(text("""
                INSERT INTO users (tg_id, tg_chat_id, tg_username, full_name)
                VALUES (:tg_id, :tg_chat_id, :tg_username, :full_name)
            """), {
                'tg_id': tg_id,
                'tg_chat_id': tg_chat_id,
                'tg_username': tg_username,
                'full_name': full_name
            })
            session.commit()
            print(f"User with tg_id {tg_id} added successfully.")
        except IntegrityError:
            print(f"User with tg_id {tg_id} already exists.")
            session.rollback()
        except Exception as e:
            print(f"An error occurred: {e}")
            session.rollback()

def add_question(specialist_type: str, tg_id: int, question_text: str):
    with Session() as session:
        try:
            session.execute(text("""
                INSERT INTO questions (specialist_type, user_id, question_text, status)
                VALUES (:specialist_type, :user_id, :question_text, 'NEW')
            """), {
                'specialist_type': specialist_type,
                'user_id': tg_id,
                'question_text': question_text
            })
            session.commit()
            print("Question added successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
            session.rollback()