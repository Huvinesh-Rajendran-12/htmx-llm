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
    created_at:str
    updated_at:str
    session_id:str
    user_prompt: str
    llm_response: str
    ratings: int
    message_feedback: str
    time_taken: float

    def __getitem__(self, key: str):
        if key == 'id':
            return self.id
        elif key == 'created_at':
            return self.created_at
        elif key == 'updated_at':
            return self.updated_at
        elif key == 'session_id':
            return self.session_id
        elif key == 'user_prompt':
            return self.user_prompt
        elif key == 'llm_response':
            return self.llm_response
        elif key == 'ratings':
            return self.ratings
        elif key == 'message_feedback':
            return self.message_feedback
        elif key == 'time_taken':
            return self.time_taken
        else:
            raise KeyError(f'Invalid key: {key}')


def create_user_input(user_prompt:str , session_id:str):
    conn = sqlite3.connect("telemechatbot.db")
    cursor = conn.cursor()
    cursor.execute("insert into conversations (session_id ,user_prompt) values (?,?)", (session_id, user_prompt, ))
    conn.commit()
    cursor.close()
    conn.close()


def update_conversation(llm_response:str, session_id:str):
    print(session_id)
    conn = sqlite3.connect("telemechatbot.db")
    select_query = "SELECT * FROM conversations WHERE session_id = ? ORDER BY created_at  DESC LIMIT 1"
    cursor = conn.cursor()
    cursor.execute(select_query, (session_id,))
    latest_record : Conversation = cursor.fetchone()
    print(latest_record)
    if latest_record:
        id = latest_record['id']
        print(id)
        cursor.execute("UPDATE conversations SET llm_response = ? WHERE id = ?", (llm_response, id, ))
        conn.commit()
    cursor.close()
    conn.close()
    
def get_all_conversations() -> list[Conversation]:
    conn = sqlite3.connect("telemechatbot.db")
    cursor = conn.cursor()
    cursor.execute("select * from conversations")
    conversations : list[Conversation] = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return conversations
    
def update_feedback(ratings:int, feedback:str, session_id:str):
    conn = sqlite3.connect("telemechatbot.db")
    cursor = conn.cursor()
    cursor.execute("update conversations set ratings = ? , user_feedback = ? where session_id = ?", (ratings, feedback, session_id,))
    conn.commit()
    cursor.close()
    conn.close()

     
def get_session_conversation(session_id:str) -> list[Conversation]:
    conn = sqlite3.connect("telemechatbot.db")
    cursor = conn.cursor()
    cursor.execute("select * from conversations where session_id = ?", (session_id,))
    conversation : list[Conversation]= cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return conversation
