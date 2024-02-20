
CREATE TABLE conversations (
  id SERIAL PRIMARY KEY,
  session_id VARCHAR(255),
  user_prompt TEXT DEFAULT "",
  llm_response TEXT DEFAULT "",
  ratings INTEGER DEFAULT 0,
  message_feedback TEXT DEFAULT "",
  time_taken FLOAT DEFAULT 0.0
);

CREATE TABLE admin(
    id SERIAL PRIMARY KEY,
    username VARCHAR(255),
    password VARCHAR(255)
);


