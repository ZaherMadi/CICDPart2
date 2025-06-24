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
    accept = request.headers.get("accept", "")

    if "text/html" in accept:
        return HTMLResponse(
content="""
<head>
    <link rel="icon" href="https://upload.wikimedia.org/wikipedia/commons/6/67/Borussia_Dortmund_logo.svg" type="image/svg+xml">
    <title>API Borussia Style</title>
</head>
<body style="
    background-image: url('https://wallpapercave.com/wp/wp4308367.jpg');
    background-size: cover;
    color: white;
    font-family: Arial, sans-serif;
    padding: 40px;
    text-shadow: 1px 1px 3px black;
">
    <img src="https://upload.wikimedia.org/wikipedia/commons/6/67/Borussia_Dortmund_logo.svg" alt="Dortmund Logo" style="height: 100px;">
    <p>Bienvenue sur la page d’accueil de l’API!</p>
    <p>Si vous voyez cette page, c’est que vous vous êtes connecté à l’API via un navigateur.</p>
    <p>Normalement, une API est faite pour être utilisée avec un outil comme <strong>Postman</strong>, <strong>Thunder Client</strong> ou directement depuis un frontend.</p>
    <p>Cette page est juste là pour vous souhaiter la bienvenue 😊</p>
    <p>Vous pouvez à présent aller sur : <a href="/users" style="color: #ffcc00;">/users</a></p>
</body>
""",
            status_code=200
        )

    return JSONResponse(
        content={"message": "✅ API OK 👌"},
        status_code=200
    )


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



