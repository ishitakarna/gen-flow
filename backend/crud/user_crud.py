from sqlalchemy.orm import Session
from sqlalchemy import text

def verify_login(db: Session, emailAddress, pwdHash):
    query = text('select * from Users where emailAddress=\''+emailAddress+'\' and pwdHash=\''+pwdHash+'\'')
    result = db.execute(query)
    user = result.fetchall()

    if len(user)==0:
        return {"status": False, "message": "Incorrect Email/Pwd"}

    query1 = text('select * from Businesses where businessId='+str(user[0]['businessId']))
    businessData = db.execute(query1).fetchone()
    return {"status": True, "message": "Successful", "user": user[0], "business": businessData}


