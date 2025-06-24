const express = require("express");
const mysql = require("mysql2/promise");

const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const pool = mysql.createPool({
  host: process.env.MYSQL_HOST,
  user: process.env.MYSQL_USER,
  password: process.env.MYSQL_PASSWORD,
  database: process.env.MYSQL_DATABASE,
  port: 3306
});

app.get("/", (req, res) => {
  const html = `
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
  `;
  res.send(html);
});

app.get("/users", async (req, res) => {
  try {
    const [rows] = await pool.query("SELECT * FROM Utilisateurs");
    res.json({ utilisateurs: rows });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post("/users", async (req, res) => {
  const { lastName, firstName, birthDate, postalCode, city, email } = req.body;
  try {
    await pool.query(
      `INSERT INTO Utilisateurs (Nom, Prenom, Naissance, Postal, Ville, Email)
       VALUES (?, ?, ?, ?, ?, ?)`,
      [lastName, firstName, birthDate, postalCode, city, email]
    );
    res.json({ message: "✅ Utilisateur ajouté avec succès" });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = app; // Important pour Vercel
