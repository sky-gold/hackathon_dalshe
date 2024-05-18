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

def is_specialist(tg_id: int):
    with Session() as session:
        result = session.execute(text("SELECT COUNT(*) FROM specialists WHERE tg_id = :tg_id"), {'tg_id': tg_id}).scalar()
        return result > 0

def get_specialist_types(tg_id: int):
    with Session() as session:
        result = session.execute(text("SELECT type FROM specialists WHERE tg_id = :tg_id"), {'tg_id': tg_id}).fetchall()
        return [row[0] for row in result]

def get_all_questions(td_id: int):
    #Возвращает list вопросов
    types = get_specialist_types(tg_id)
    with Session() as session:
        params = {'types': tuple(types), 'status': 'NEW'}
        query = text("SELECT id FROM questions WHERE specialist_type IN :types AND status = :status")
        result = session.execute(query, params).fetchall()
        return [row[0] for row in result]


def get_question(question_id: int):
    #возвращает вопрос по индексу
    with Session() as session:
        try:
            result = session.execute(text("SELECT * FROM users WHERE id = :id"), {'id': question_id}).fetchone()
            if result:
                return dict(result)
            else:
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


def try_answer_question(question_id: int, tg_id: int):
    #Возвращает True если было NEW и удалось изменить и False иначе
    with Session() as session:
        try:
            query = text("""
                UPDATE questions
                SET answered_by = :tg_id
                WHERE id = :question_id AND (status = 'NEW' OR status = 'IN_PROGRESS')
            """)
            session.execute(query, {'question_id': question_id, 'tg_id': tg_id})
            rows_updated = session.execute(text("SELECT row_count();")).scalar()
            session.commit()
            return rows_updated > 0
        except Exception as e:
            print(f"An error occurred: {e}")
            session.rollback()
            return False
