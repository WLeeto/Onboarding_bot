from fastapi import FastAPI
from database.requests import database

app = FastAPI()
# uvicorn fastapi_main:app --reload

db = database()


@app.get("/users")
def get_users():
    all_users = db.find_all_users()
    return all_users


# todo Сделать валидаторы для полей с датами. Настроить возврат ошибок из консоли
@app.post("/users")
def add_new_user(tg_id: int, first_name: str, surname: str, job_title: str, tg_name: str = None, photo: str = None,
                 hired_at: str = None, middle_name: str = None, nickname: str = None, department_id: int = None,
                 organization_id: int = None, user_id: int = None, fired_at: str = None, date_of_birth: str = None,
                 status: str = None, timezone: str = None):
    new_user = db.add_new_user(
        tg_id=tg_id,
        first_name=first_name,
        surname=surname,
        job_title=job_title,
        tg_name=tg_name,
        photo=photo,
        hired_at=hired_at,
        middle_name=middle_name,
        nickname=nickname,
        department_id=department_id,
        organization_id=organization_id,
        user_id=user_id,
        fired_at=fired_at,
        date_of_birth=date_of_birth,
        status=status,
        timezone=timezone
    )

    return {"status": 200, "data": new_user}
