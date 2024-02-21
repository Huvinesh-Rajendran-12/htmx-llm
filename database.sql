
CREATE TABLE conversations (
  id INTEGER PRIMARY KEY,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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


