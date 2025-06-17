import mysql.connector
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["+"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Create a connection to the database
conn = mysql.connector.connect(
    database=os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    port=3306,
    host=os.getenv("MYSQL_HOST"))

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
      <head>
        <title>Bienvenue</title>
      </head>
      <body>
        <h1>Bienvenue sur l'API</h1>
        <p>Ceci est une réponse HTML simple.</p>
      </body>
    </html>
    """"


@app.get("/users")
async def get_users():
    cursor = conn.cursor()
    sql_select_Query = "select * from utilisateur"
    cursor.execute(sql_select_Query)
    # get all records
    records = cursor.fetchall()
    print("Total number of rows in table: ", cursor.rowcount)
    # renvoyer nos données et 200 code KO
    return {'utilisateurs': records}


