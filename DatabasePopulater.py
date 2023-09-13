import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Monty1010",
    database="journal_publishing_policy"
)

mycursor = db.cursor()
