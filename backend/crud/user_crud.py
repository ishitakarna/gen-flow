from sqlalchemy.orm import Session
from sqlalchemy import text

def verify_login(db: Session, emailAddress, pwdHash):
    query = text('select * from Users where emailAddress=\''+emailAddress+'\' and pwdHash=\''+pwdHash+'\'')
    result = db.execute(query)
    user = result.fetchall()
    if len(user)==0:
        return {"status": False, "message": "Incorrect Email/Pwd"}
    return {"status": True, "message": "Successful", "user": user[0]}


