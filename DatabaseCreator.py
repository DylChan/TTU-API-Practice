import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Monty1010",
)

mycursor = db.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS journal_publishing_policy")
mycursor.execute("USE journal_publishing_policy")
# decide which info you want to save from the json file, then make tables for each of those
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS items (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), sherpa_ID VARCHAR(255), published_allowed BOOLEAN, published_conditions VARCHAR(255), published_embargo VARCHAR(255), published_license VARCHAR(255), accepted_allowed BOOLEAN, accepted_conditions VARCHAR(255), accepted_embargo VARCHAR(255), accepted_license VARCHAR(255), submitted_allowed BOOLEAN, submitted_conditions VARCHAR(255), submitted_embargo VARCHAR(255), submitted_license VARCHAR(255))")
mycursor.execute("SHOW DATABASES")

for data in mycursor:
    print(data)
