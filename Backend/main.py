from fastapi import FastAPI
import mysql.connector

app = FastAPI()

@app.get("/")
def read_root():
    return {"msg": "Hello from FastAPI"}

@app.get("/db")
def db_test():
    conn = mysql.connector.connect(
        host="mysql-service",
        user="user",
        password="password",
        database="appdb"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT 'Hello from MySQL!'")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return {"msg": result[0]}
