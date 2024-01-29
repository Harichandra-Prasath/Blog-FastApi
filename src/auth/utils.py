import bcrypt


def get_password_hash(plain_password:str):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode('utf-8'),salt=salt)

def verify_password(plain_password:str,hashed_password:str):
    return bcrypt.checkpw(plain_password.encode('utf-8'),hashed_password)