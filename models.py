import sqlite3
from dataclasses import dataclass

@dataclass
class Admin:
    id: int
    username: str
    password: str


@dataclass
class Conversation:
    id: int
    session_id:str
    user_prompt: str
    llm_response: str
    ratings: int
    message_feedback: str
    time_taken: int


def create_conversation(user_prompt:str, llm_response:str):
    conn = sqlite3.connect("telemechatbot.db")
    cursor = conn.cursor()
    cursor.execute("insert into conversations (user_prompt, llm_response) values (?, ?)", (user_prompt, llm_response))
    conn.commit()
    conn.close()
    
 
def get_all_conversations() -> list[Conversation]:
    conn = sqlite3.connect("telemechatbot.db")
    cursor = conn.cursor()
    cursor.execute("select * from conversations")
    conversations : list[Conversation] = cursor.fetchall()
    conn.commit()
    conn.close()
    return conversations
    
     
def get_session_conversation(session_id:str) -> list[Conversation]:
    conn = sqlite3.connect("telemechatbot.db")
    cursor = conn.cursor()
    cursor.execute("select * from conversations where session_id = ?", (session_id))
    conversation : list[Conversation]= cursor.fetchall()
    conn.commit()
    conn.close()
    return conversation
