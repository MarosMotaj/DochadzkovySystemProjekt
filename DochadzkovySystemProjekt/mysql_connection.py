import mysql.connector

# Host je IP adresa PC kde bezi MySQL databaza
# user a password je uzivatel z MySQL servra, vytvoreny na MySQL serveri


def print_data():
    mysql_database = mysql.connector.connect(host="",
                                             user="",
                                             password="",
                                             database="")


    my_cursor = mysql_database.cursor()
    # Vykona zadane SQL prikazy
    my_cursor.execute("select * from employees")

    # Vypise data na zadanom indexe
    data = my_cursor.fetchall().pop(0)

    # for i in data:
    #     print(i)
    return data[1]+" "+data[2]

    # mysql_database.close()