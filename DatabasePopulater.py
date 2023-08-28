import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Monty1010",
    database="sherpa_romeo"
)

mycursor = db.cursor()
