import bcrypt
import jwt
import datetime

def get_password_hash(plain_password:str):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode('utf-8'),salt=salt)

def verify_password(plain_password:str,hashed_password:str):
    return bcrypt.checkpw(plain_password.encode('utf-8'),hashed_password)
    

def generate_jwt(username):
    token = jwt.encode({"username":username,
                        "exp":datetime.datetime.now(tz=datetime.timezone.utc)+datetime.timedelta(days=30)},
                         key="Secret",
                         algorithm="HS256",
                         )
    return token