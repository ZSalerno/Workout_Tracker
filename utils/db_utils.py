from sqlalchemy import create_engine

_ENGINE = "mysql+mysqldb://python_user:PythonConn149147@localhost/workout_db"

def create_connection(host, user, pw, db):
    db = mysql.connector.connect(
        host=host,
        user=user,
        passwd=pw,
        database=db,
    )
    return db

