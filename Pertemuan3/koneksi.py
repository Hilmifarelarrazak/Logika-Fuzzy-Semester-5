import mysql.connector


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_fuzzy"
)

print("Koneksi database berhasil!")

db.close()