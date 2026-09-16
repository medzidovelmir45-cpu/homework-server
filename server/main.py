from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import json
import os
from datetime import datetime

app = FastAPI(title="Homework API")

ADMIN_SECRET = "my_secret_password_123"
DB_FILE = "homework.json"

# Гарантированное создание файла при запуске
if not os.path.exists(DB_FILE):
    initial_data = [
        {
            "id": 1,
            "subject": "Дизайн UI/UX",
            "task": "Сделать макет карточки в Figma",
            "date_target": "На завтра",
            "answer": "https://i.imgur.com/sample.jpg",
            "created_at": datetime.now().strftime("%d.%m.%Y %H:%M")
        }
    ]
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(initial_data, f, ensure_ascii=False, indent=2)

def load_db():
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class HomeworkCreate(BaseModel):
    subject: str
    task: str
    date_target: str
    answer: str = ""

@app.get("/homework")
def get_homework():
    return list(reversed(load_db()))

@app.post("/homework")
def add_homework(item: HomeworkCreate, secret: str = Header(None)):
    if secret != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Неверный пароль!")
    
    db_homework = load_db()
    now_str = datetime.now().strftime("%d.%m.%Y %H:%M")
    new_id = max([h.get("id", 0) for h in db_homework], default=0) + 1
    
    new_item = {
        "id": new_id,
        "subject": item.subject,
        "task": item.task,
        "date_target": item.date_target,
        "answer": item.answer,
        "created_at": now_str
    }
    
    db_homework.append(new_item)
    save_db(db_homework)
    return {"status": "ok", "message": "ДЗ добавлено!", "item": new_item}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
