CREATE TABLE users (
    tg_id BIGINT PRIMARY KEY,
    tg_username VARCHAR(255),
    full_name VARCHAR(255)
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    specialist_type VARCHAR(255),
    user_id BIGINT REFERENCES users(tg_id),
    question_text TEXT,
    answer TEXT,
    status VARCHAR(20) CHECK (status IN ('NEW', 'IN_PROCESS', 'DONE'))
);

CREATE TABLE admin (
    tg_id BIGINT,
    tg_username VARCHAR(255)
);

INSERT INTO admin (tg_id, tg_username)
VALUES (738035643, 'Leloush_0');