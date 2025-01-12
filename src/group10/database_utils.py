import mysql.connector as mysql

DB_NAME = "defaultdb"
DB_USER = "avnadmin"
DB_PASSWORD = "AVNS_QXs1v9qBTveDtLIXZfW"
DB_HOST = "mysql-374f4726-majidnamiiiii-e945.a.aivencloud.com"
DB_PORT = "11741"
DB_URL = "mysql://avnadmin:AVNS_QXs1v9qBTveDtLIXZfW@mysql-374f4726-majidnamiiiii-e945.a.aivencloud.com:11741/defaultdb?ssl-mode=REQUIRED"


def create_db_connection(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME):
    mydb = None
    try:
        mydb = mysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
        )
        print("Connection to MySQL DB successful")
    except Exception as e:
        print(f"The error '{e}' occurred")

    return mydb
