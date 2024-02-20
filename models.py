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


def create_user_input(user_prompt:str , session_id:str):
    conn = sqlite3.connect("telemechatbot.db")
    cursor = conn.cursor()
    cursor.execute("insert into conversations (session_id ,user_prompt) values (?,?)", (user_prompt, session_id,))
    conn.commit()
    conn.close()


def create_conversation(llm_response:str, session_id:str):
    conn = sqlite3.connect("telemechatbot.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE conversations SET llm_response = ? WHERE session_id = ?", (llm_response, session_id))
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
    
def update_feedback(ratings:int, feedback:str, session_id:str):
    conn = sqlite3.connect("telemechatbot.db")
    cursor = conn.cursor()
    cursor.execute("update conversations set ratings = ? , user_feedback = ? where session_id = ?", (ratings, feedback, session_id,))
    conn.commit()
    conn.close()

     
def get_session_conversation(session_id:str) -> list[Conversation]:
    conn = sqlite3.connect("telemechatbot.db")
    cursor = conn.cursor()
    cursor.execute("select * from conversations where session_id = ?", (session_id,))
    conversation : list[Conversation]= cursor.fetchall()
    conn.commit()
    conn.close()
    return conversation
