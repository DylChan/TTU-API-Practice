import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Monty1010",
    database="sherpa_romeo"
)

mycursor = db.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS sherpa_romeo")
mycursor.execute("USE sherpa_romeo")
# decide which info you want to save from the json file, then make tables for each of those
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS items (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255))")
mycursor.execute("SHOW DATABASES")

for data in mycursor:
    print(data)
