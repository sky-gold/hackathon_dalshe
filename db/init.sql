CREATE TABLE users (
    tg_id BIGINT PRIMARY KEY,
    tg_chat_id BIGINT,
    tg_username VARCHAR(255),
    full_name VARCHAR(255)
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    specialist_type VARCHAR(255),
    user_id BIGINT REFERENCES users(tg_id),
    question_text TEXT,
    answered_by BIGINT,
    answer TEXT,
    status VARCHAR(20) CHECK (status IN ('NEW', 'IN_PROCESS', 'DONE'))
);

CREATE TABLE live_chat_connections (
    user_id BIGINT REFERENCES users(tg_id),
    specialist_type VARCHAR(255),
    specialist_id BIGINT,
    status VARCHAR(20) CHECK (status IN ('NEW', 'IN_PROCESS', 'DONE')),
    PRIMARY KEY (user_id, specialist_id)
);