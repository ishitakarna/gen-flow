from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import text

def get_users_test(db: Session):
    query = text('select * from Users')
    result = db.execute(query)
    names = [row[0] for row in result]
    print(names)
    return {"Hehe": True}