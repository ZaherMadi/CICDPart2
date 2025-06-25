import mysql.connector
import os
from fastapi import FastAPI, Request, Form, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import Form # pour la gestion des formulaires
import jwt # pour la gestion des tokens JWT
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError # pour la gestion des tokens JWT
from pydantic import BaseModel # pour la validation des données
from typing import Optional  

ALGORITHM = "HS256"  # Algorithme de signature pour JWT 
SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # Clé secrète pour signer les tokens JWT

class Login(BaseModel):
    email: str
    password: str

class User(BaseModel):
    nom: str
    prenom: str
    email: str
    date_naissance: str
    pays: str
    ville: str
    code_postal: str

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Create a connection to the database
def get_db_connection():
    if os.getenv("VERCEL_ENV") == "production":
        return mysql.connector.connect(
            host=os.getenv("ALWAYSDATA_HOST", "mysql-51bvb.alwaysdata.net"),
            port=3306,
            user=os.getenv("MYSQL_USER", "51BVB"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE", "51bvb_formulaire"),
            charset='utf8mb4',
            use_unicode=True,
            autocommit=True
        )
    else:
        # For local development, use environment variables
        return mysql.connector.connect(
            database=os.getenv("MYSQL_DATABASE"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD", os.getenv("MYSQL_ROOT_PASSWORD")),
            port=3306, 
            host=os.getenv("MYSQL_HOST", "localhost")
        )


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
    <p>Vous pouvez à présent aller sur : <a href="/users" style="color: #ffcc00;">/users</a> afin d'avoir la liste des utilisateurs</p>
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
    try:
        conn = get_db_connection()   # ✅ Ouvre la connexion ici
        cursor = conn.cursor()
        sql_select_Query = "SELECT * FROM Utilisateurs"
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        conn.close()  # ✅ Toujours fermer la connexion
        return {'Utilisateurs': records}
    except Exception as e:
        print("Erreur :", e)
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/users")
async def add_user(
    lastName: str = Form(...),
    firstName: str = Form(...),
    birthDate: str = Form(...),
    postalCode: str = Form(...),
    city: str = Form(...),
    email: str = Form(...)):
    try:
        conn = get_db_connection()  # ✅ Ajoute cette ligne
        cursor = conn.cursor()
        sql = """
        INSERT INTO Utilisateurs (Nom, Prenom, Naissance, Postal, Ville, Email)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (lastName, firstName, birthDate, postalCode, city, email)
        cursor.execute(sql, values)
        conn.commit()
        conn.close()
        return {"message": "✅ Utilisateur ajouté avec succès"}
    except Exception as e:
        print("Erreur SQL :", e)
        return JSONResponse(content={"error": str(e)}, status_code=500)


# ==== LOGIN ====

@app.post("/login")
async def login_user(login: Login):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Administrateurs WHERE email = %s AND password = %s", (login.email, login.password))
        records = cursor.fetchall()
        conn.close()

        if len(records) > 0:
            # Durée du token (1h ici)
            expiration = datetime.utcnow() + timedelta(hours=1)
            token = jwt.encode({"email": login.email, "exp": expiration}, SECRET_KEY, algorithm=ALGORITHM)
            return {"token": token, "message": "Connexion réussie"}
        else:
            raise HTTPException(status_code=401, detail="Identifiants incorrects")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

# ==== DELETE UTILISATEUR ====

@app.delete("/users/{user_id}")
async def delete_user(user_id: int, authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token manquant ou invalide")

    token = authorization.split(" ")[1]
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Utilisateurs WHERE id = %s", (user_id,))
        conn.commit()
        deleted = cursor.rowcount
        conn.close()

        if deleted:
            return {"message": f"Utilisateur {user_id} supprimé ✅"}
        else:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expiré")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalide")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur suppression: {str(e)}")