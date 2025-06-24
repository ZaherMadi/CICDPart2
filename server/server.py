import mysql.connector
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import Form

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# #Create a connection to the database
# conn = mysql.connector.connect(
#     database=os.getenv("MYSQL_DATABASE"),
#     user=os.getenv("MYSQL_USER"),
#     password=os.getenv("MYSQL_PASSWORD"),
#     port=3306,
#     host=os.getenv("MYSQL_HOST"))

@app.get("/")
async def home(request: Request):
    return { "message": "Bienvenue sur l'API de gestion des utilisateurs !"}


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

@app.post("/users")
async def add_user(
    lastName: str = Form(...),
    firstName: str = Form(...),
    birthDate: str = Form(...),
    postalCode: str = Form(...),
    city: str = Form(...),
    email: str = Form(...)
):
    try:
        cursor = conn.cursor()
        sql = """
        INSERT INTO Utilisateurs (Nom, Prenom, Naissance, Postal, Ville, Email)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (lastName, firstName, birthDate, postalCode, city, email)
        cursor.execute(sql, values)
        conn.commit()
        return {"message": "✅ Utilisateur ajouté avec succès"}
    except Exception as e:
        print("Erreur SQL :", e)
        return JSONResponse(content={"error": str(e)}, status_code=500)



