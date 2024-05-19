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

def add_user(tg_id: int, tg_username: str, full_name: str):
    with Session() as session:
        try:
            session.execute(text("""
                INSERT INTO users (tg_id, tg_username, full_name)
                VALUES (:tg_id, :tg_username, :full_name)
            """), {
                'tg_id': tg_id,
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
            result = session.execute(text("""
                INSERT INTO questions (specialist_type, user_id, question_text, status)
                VALUES (:specialist_type, :user_id, :question_text, 'NEW')
                RETURNING id
            """), {
                'specialist_type': specialist_type,
                'user_id': tg_id,
                'question_text': question_text
            })
            session.commit()
            print("Question added successfully.")
            return result.scalar()
        except Exception as e:
            print(f"An error occurred: {e}")
            session.rollback()

def is_admin(tg_id: int):
    with Session() as session:
        result = session.execute(text("SELECT COUNT(*) FROM admin WHERE tg_id = :tg_id"), {'tg_id': tg_id}).scalar()
        return result > 0

def get_all_questions():
    #Возвращает list id вопросов
    with Session() as session:
        result = session.execute(text("SELECT id FROM questions")).fetchall()
        if not result:
            return []
        return [row[0] for row in result]


def get_question(question_id: int):
    #возвращает вопрос по индексу
    with Session() as session:
        try:
            result = session.execute(text(f"SELECT * FROM questions WHERE id = {question_id}")).fetchone()
            if result:
                return {"id": result[0],
                        "datetime": result[1],
                        "specialist_type": result[2],
                        "user_id": result[3],
                        "question_text": result[4],
                        "answer": result[5],
                        "status": result[6]
                        }

            else:
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


def answer_question(question_id: int, answer: text):
    with Session() as session:
        sql_query = text("""
            UPDATE questions
            SET status = :status, answer = :answer
            WHERE id = :question_id
        """)
        session.execute(sql_query, {'status': 'DONE', 'answer': answer, 'question_id': question_id})
        session.commit()
